from jinja2 import Environment, FileSystemLoader
from os.path import dirname
from api_validator.tools.oasdiff import OasdiffOutput


def list_length(lst):
    return len(lst)


class GitHubJobSummary:
    def __init__(
            self,
            oasdiff_outputs: [OasdiffOutput],
            overall_elapsed_time: float = 0.0,
    ):
        # sort oasdiff_outputs by language and then by repository_url
        self.oasdiff_outputs = sorted(oasdiff_outputs, key=lambda x: (x.language, x.repository_url))
        self.report_data = []
        self.overall_elapsed_time = overall_elapsed_time
        for oasdiff in self.oasdiff_outputs:
            self.report_data.append(oasdiff.report())

    def github_step_summary(self) -> str:
        """
        Generate GitHub Job Summary:
        https://github.blog/2022-05-09-supercharging-github-actions-with-job-summaries/#create-summaries
        """
        # template_contents = self.report()
        # TODO: Create an overall summary of deleted endpoints vs new endpoints
        # we also need to report
        total_discoveries = 0
        total_deletions = 0
        total_additions = 0
        total_changes = 0
        elapsed_time = 0
        success_rates = []
        for report in self.report_data:
            total_discoveries += report["total_discovered"]
            total_deletions += len(report["deleted_endpoints"])
            total_additions += len(report["added_endpoints"])
            total_changes += len(report["modified_endpoints"])
            elapsed_time += report["elapsed_time"]
            success_rates.append(report["success_rate"])

        try:
            average_success_rate = sum(success_rates) / len(success_rates)
        except ZeroDivisionError:
            average_success_rate = 0.0
        all_total_endpoints = total_discoveries + total_deletions
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        # fmt: off
        summary_description = f"""The API Extractor performed scans on **{len(self.oasdiff_outputs)}** repositories to discover API endpoints. There were **{all_total_endpoints}** endpoints to be discovered. NightVision found **{total_discoveries}** endpoints. Of these, **{total_additions}** are new endpoints (not declared in the existing Swagger doc). 
        
**Undiscovered endpoints**: NightVision did not discover **{total_deletions}** endpoints. These endpoints were declared in the existing Swagger doc, but our tool did not discover it.

**Average success rate**: {average_success_rate:.2f}%

**Execution Time**: The API Extraction process took {minutes} minutes and {seconds} seconds to run across all {len(self.oasdiff_outputs)} jobs, although we shortened the time to execute by applying multithreading."""
        # fmt: on
        template_path = dirname(__file__)
        env = Environment(loader=FileSystemLoader(template_path))
        env.filters["list_length"] = list_length
        template = env.get_template("job_summary.md.j2")
        return template.render(summary_description=summary_description, report_data=self.report_data)
