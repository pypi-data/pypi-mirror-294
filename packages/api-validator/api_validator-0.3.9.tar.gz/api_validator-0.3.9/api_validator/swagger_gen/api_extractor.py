import time
from os.path import exists, join, dirname
from os import remove, environ, cpu_count
import threading
from api_validator.diff_utils.job_summary import GitHubJobSummary
from api_validator.diff_utils.jobs import JobsContainer, read_jobs_from_yaml


def api_extractor(jobs_container: JobsContainer, output_file: str, binary_path: str = None, internal: bool = False):
    """Run API Extraction with multi-threading"""
    oasdiff_outputs = []
    overall_start_time = time.time()

    def process_extraction(job):
        print(f"\t{job.owner}/{job.repo_name}: Working on Job: {job.name}")
        # Print job details
        print(
            f"\t{job.owner}/{job.repo_name}: Repo: {job.repo}, Swagger File: {job.swagger_file}, Language: {job.language}")
        # Download the base Swagger file
        print(f"\t{job.owner}/{job.repo_name}: Downloading base Swagger file...")
        job.download_base_swagger()

        # Run the extraction process
        start_time = time.time()
        print(f"\t{job.owner}/{job.repo_name}: Running extraction...")
        job.run_extraction(binary_path=binary_path, internal=internal)
        end_time = time.time()
        elapsed = end_time - start_time

        # Perform OASDiff operation
        print(f"\t{job.owner}/{job.repo_name}: Performing OASDiff operation...")
        oasdiff_output = job.oasdiff(elapsed_time=elapsed)
        oasdiff_outputs.append(oasdiff_output)

        print(f"\t{job.owner}/{job.repo_name}: Completed work on Job: {job.name}\n")

    def clone_repository(job):
        # Clone the repository
        print(f"\t{job.owner}/{job.repo_name}: Cloning...")
        if exists(job.local_repo):
            print(f"\t{job.owner}/{job.repo_name}: Local repo already exists. Skipping clone.")
        else:
            job.clone()

    def clone_for_chunk(jobs_chunk, thread_id, progress_tracker):
        for job in jobs_chunk:
            clone_repository(job)
            progress_tracker[thread_id] = f"Repository cloned for: {job.name}"
            print(f"{job.owner}/{job.repo_name}: Thread {thread_id} progress: {progress_tracker[thread_id]}")

    def extraction_for_chunk(jobs_chunk, thread_id, progress_tracker):
        for job in jobs_chunk:
            process_extraction(job)  # Existing job processing logic
            progress_tracker[thread_id] = f"Completed: {job.name}"
            print(f"{job.owner}/{job.repo_name}: Thread {thread_id} progress: {progress_tracker[thread_id]}")

    def process_action_for_chunks(jobs_chunks, action, message):
        threads = []
        for i, chunk in enumerate(jobs_chunks):
            job_names = ", ".join([job.name for job in chunk])
            print(f"Thread {i} will process {message} for jobs: {job_names}")
            thread = threading.Thread(target=action, args=(chunk, i, progress_tracker))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    # Calculate the number of threads to use
    num_cores = cpu_count()
    num_threads = max(2 * num_cores, 4)
    # Never have more threads than the number of jobs
    num_threads = min(num_threads, len(jobs_container))

    chunk_size = max(len(jobs_container) // num_threads, 1)
    remainder = len(jobs_container) % num_threads
    # chunks = [jobs_container[i:i + chunk_size] for i in range(0, len(jobs_container), chunk_size)]
    chunks = []
    start = 0

    for i in range(num_threads):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunk = jobs_container[start:end]
        chunks.append(chunk)
        start = end

    progress_tracker = {}

    process_action_for_chunks(chunks, clone_for_chunk, "cloning")
    process_action_for_chunks(chunks, extraction_for_chunk, "extraction")

    # Print final progress status
    for i in range(num_threads):
        print(f"Thread {i} final status: {progress_tracker.get(i, 'Completed')}")
    print("All threads completed.")

    # Summarize and save results
    overall_end_time = time.time()
    overall_elapsed = overall_end_time - overall_start_time
    job_summary = GitHubJobSummary(oasdiff_outputs, overall_elapsed_time=overall_elapsed)
    step_summary = job_summary.github_step_summary()

    if exists(output_file):
        remove(output_file)
    with open(output_file, "w") as f:
        f.write(step_summary)
    print(f"Saved {output_file}")

    # If not running in GitHub actions, clean it up
    if "GITHUB_ACTIONS" in environ:
        print("Cleaning up old repositories")
        for job in jobs_container:
            # Clean up the repository
            print(f"\t{job.owner}/{job.repo_name}: Cleaning up...")
            job.clean()
