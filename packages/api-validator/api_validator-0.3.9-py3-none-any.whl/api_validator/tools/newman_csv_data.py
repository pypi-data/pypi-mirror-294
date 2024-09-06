import pandas as pd
from typing import Dict, List, Union
from jinja2 import Environment, FileSystemLoader
from os.path import dirname, exists
from os import remove


class NewmanData:
    def __init__(self, file_path: str) -> None:
        self.data = pd.read_csv(file_path)
        self.apps: Dict[str, AppAnalysis] = self.get_apps()

    def get_apps(self) -> Dict[str, 'AppAnalysis']:
        app_names = self.data['app_name'].unique()
        return {name: AppAnalysis(self.data[self.data['app_name'] == name]) for name in app_names}

    def __repr__(self) -> str:
        app_names = list(self.apps.keys())
        app_names.sort()
        return f'NewmanData ({len(self.apps)} apps: {", ".join(app_names)})'


class AppAnalysis:
    def __init__(self, app_data: pd.DataFrame) -> None:
        """Initialize the AppAnalysis with specific application data."""
        self.app_data = app_data

    def get_status_code_info(self, codes: List[Union[int, str]]) -> Dict[Union[int, str], Dict[str, Union[int, float, List[Dict[str, str]]]]]:
        code_info = {}
        total = self.app_data.shape[0]
        for code in codes:
            if code == 'Skipped':
                filtered_data = self.app_data[self.app_data['code'].isna()]
            else:
                filtered_data = self.app_data[self.app_data['code'] == code]
                code = int(code) if pd.api.types.is_number(code) else code

            count = filtered_data.shape[0]
            percentage = (count / total) * 100 if total > 0 else 0
            endpoints = [{'path': row['url'], 'method': row.get('method', 'Unknown')} for _, row in filtered_data.iterrows()]

            code_info[code] = {'count': count, 'percentage': percentage, 'endpoints': endpoints}
        return code_info

    def get_all_status_code_info(self) -> Dict[Union[int, str], Dict[str, Union[int, float, List[str]]]]:
        """
        Get information for all status codes present in the application data.
        :return: Dictionary with count, percentage, and paths for each status code.
        """
        all_codes = self.app_data['code'].unique().tolist()
        # Adjust to handle NaN values and non-numeric values
        all_codes = ['Skipped' if pd.isna(code) else int(code) if pd.api.types.is_number(code) else code for code in all_codes]
        return self.get_status_code_info(all_codes)


class AppManager:
    def __init__(self, newman_data: NewmanData) -> None:
        self.apps = newman_data.apps

    def get_sorted_apps(self, code: Union[int, List[int]]) -> Dict[str, Dict[str, Union[int, float, List[str]]]]:
        """
        Example usage:
            sorted_apps_200 = app_manager.get_sorted_apps(200)
            print(sorted_apps_200)

        Output:
            {'nodejs-goof': {200: {'count': 9, 'percentage': 50.0, 'paths': ['http://localhost:3001/', 'http://localhost:3001/about_new?device=<string>', 'http://localhost:3001/account_details', 'http://localhost:3001/admin', 'http://localhost:3001/chat', 'http://localhost:3001/edit/<string>', 'http://localhost:3001/import', 'http://localhost:3001/login?redirectPage=<string>', 'http://localhost:3001/logout']}}, 'javaspringvulny-api': {200: {'count': 28, 'percentage': 71.7948717948718, 'paths': ['https://localhost:9000/', 'https://localhost:9000/admin', 'https://localhost:9000/admin/companies', 'https://localhost:9000/admin/payload/stream/<integer>', 'https://localhost:9000/admin/payload/<integer>', 'https://localhost:9000/admin/payloads', 'https://localhost:9000/admin/search', 'https://localhost:9000/admin/search', 'https://localhost:9000/admin/users', 'https://localhost:9000/basic-auth', 'https://localhost:9000/hidden', 'https://localhost:9000/hidden/cypress', 'https://localhost:9000/hidden/hidden2', 'https://localhost:9000/hidden/playwright', 'https://localhost:9000/hidden/selenium', 'https://localhost:9000/jwt-auth', 'https://localhost:9000/log4j?text=<string>', 'https://localhost:9000/login', 'https://localhost:9000/login-code', 'https://localhost:9000/login-form-multi', 'https://localhost:9000/login-form-multi', 'https://localhost:9000/login-multi-check', 'https://localhost:9000/payload/stream/<integer>', 'https://localhost:9000/payload/<integer>', 'https://localhost:9000/payloads', 'https://localhost:9000/search', 'https://localhost:9000/search', 'https://localhost:9000/token-auth']}}, 'govwa': {200: {'count': 20, 'percentage': 100.0, 'paths': ['http://localhost:8888/', 'http://localhost:8888/csa', 'http://localhost:8888/idor1', 'http://localhost:8888/idor1action?city=<string>&name=<string>&number=<string>&uid=<string>', 'http://localhost:8888/idor2', 'http://localhost:8888/idor2action?city=<string>&name=<string>&number=<string>&signature=<string>&uid=<string>', 'http://localhost:8888/index', 'http://localhost:8888/login?password=<string>&username=<string>', 'http://localhost:8888/login?password=<string>&username=<string>', 'http://localhost:8888/logout', 'http://localhost:8888/setlevel?level=<string>', 'http://localhost:8888/setting', 'http://localhost:8888/setup', 'http://localhost:8888/setupaction?act=<string>', 'http://localhost:8888/sqli1', 'http://localhost:8888/sqli2?uid=<string>', 'http://localhost:8888/verify?otp=<string>', 'http://localhost:8888/xss1?term=<string>', 'http://localhost:8888/xss1?term=<string>', 'http://localhost:8888/xss2?uid=<string>']}}, 'Tiredful-API': {200: {'count': 8, 'percentage': 88.88888888888889, 'paths': ['http://localhost:8000/', 'http://localhost:8000/advertisements', 'http://localhost:8000/api/v1', 'http://localhost:8000/blog', 'http://localhost:8000/exams', 'http://localhost:8000/health', 'http://localhost:8000/library', 'http://localhost:8000/trains']}}, 'crAPI': {200: {'count': 2, 'percentage': 8.0, 'paths': ['http://localhost:8888/identity/api/auth/jwks.json', 'http://localhost:8888/identity/health_check']}}, 'vuln_node_express_api': {200: {'count': 3, 'percentage': 75.0, 'paths': ['http://localhost:3000/', 'http://localhost:3000/api/search?searchText=<string>', 'http://localhost:3000/search']}}, 'VulnerableApp': {200: {'count': 1, 'percentage': 14.285714285714285, 'paths': ['http://localhost:80/VulnerabilityDefinitions']}}, 'Vulnerable-Flask-App': {200: {'count': 3, 'percentage': 21.428571428571427, 'paths': ['http://localhost:5050/', 'http://localhost:5050/xxe', 'http://localhost:5050/yaml']}}, 'alist': {200: {'count': 107, 'percentage': 98.1651376146789, 'paths': ['http://localhost:5244/', 'http://localhost:5244/api/admin/driver/info?driver=<string>', 'http://localhost:5244/api/admin/driver/list', 'http://localhost:5244/api/admin/driver/names', 'http://localhost:5244/api/admin/index/build', 'http://localhost:5244/api/admin/index/clear', 'http://localhost:5244/api/admin/index/progress', 'http://localhost:5244/api/admin/index/stop', 'http://localhost:5244/api/admin/index/update', 'http://localhost:5244/api/admin/meta/create', 'http://localhost:5244/api/admin/meta/delete?id=<string>', 'http://localhost:5244/api/admin/meta/get?id=<string>', 'http://localhost:5244/api/admin/meta/list?Page=<integer>&PerPage=<integer>', 'http://localhost:5244/api/admin/meta/update', 'http://localhost:5244/api/admin/setting/delete?key=<string>', 'http://localhost:5244/api/admin/setting/get?key=<string>&keys=<string>', 'http://localhost:5244/api/admin/setting/list?group=<string>&groups=<string>', 'http://localhost:5244/api/admin/setting/reset_token', 'http://localhost:5244/api/admin/setting/save', 'http://localhost:5244/api/admin/setting/set_aria2', 'http://localhost:5244/api/admin/setting/set_qbit', 'http://localhost:5244/api/admin/storage/create', 'http://localhost:5244/api/admin/storage/delete?id=<string>', 'http://localhost:5244/api/admin/storage/disable?id=<string>', 'http://localhost:5244/api/admin/storage/enable?id=<string>', 'http://localhost:5244/api/admin/storage/get?id=<string>', 'http://localhost:5244/api/admin/storage/list?Page=<integer>&PerPage=<integer>', 'http://localhost:5244/api/admin/storage/load_all', 'http://localhost:5244/api/admin/storage/update', 'http://localhost:5244/api/admin/task/copy/cancel?tid=<string>', 'http://localhost:5244/api/admin/task/copy/clear_done', 'http://localhost:5244/api/admin/task/copy/clear_succeeded', 'http://localhost:5244/api/admin/task/copy/delete?tid=<string>', 'http://localhost:5244/api/admin/task/copy/done', 'http://localhost:5244/api/admin/task/copy/retry?tid=<string>', 'http://localhost:5244/api/admin/task/copy/retry_failed', 'http://localhost:5244/api/admin/task/copy/undone', 'http://localhost:5244/api/admin/task/offline_download/cancel?tid=<string>', 'http://localhost:5244/api/admin/task/offline_download/clear_done', 'http://localhost:5244/api/admin/task/offline_download/clear_succeeded', 'http://localhost:5244/api/admin/task/offline_download/delete?tid=<string>', 'http://localhost:5244/api/admin/task/offline_download/done', 'http://localhost:5244/api/admin/task/offline_download/retry?tid=<string>', 'http://localhost:5244/api/admin/task/offline_download/retry_failed', 'http://localhost:5244/api/admin/task/offline_download/undone', 'http://localhost:5244/api/admin/task/offline_download_transfer/cancel?tid=<string>', 'http://localhost:5244/api/admin/task/offline_download_transfer/clear_done', 'http://localhost:5244/api/admin/task/offline_download_transfer/clear_succeeded', 'http://localhost:5244/api/admin/task/offline_download_transfer/delete?tid=<string>', 'http://localhost:5244/api/admin/task/offline_download_transfer/done', 'http://localhost:5244/api/admin/task/offline_download_transfer/retry?tid=<string>', 'http://localhost:5244/api/admin/task/offline_download_transfer/retry_failed', 'http://localhost:5244/api/admin/task/offline_download_transfer/undone', 'http://localhost:5244/api/admin/task/upload/cancel?tid=<string>', 'http://localhost:5244/api/admin/task/upload/clear_done', 'http://localhost:5244/api/admin/task/upload/clear_succeeded', 'http://localhost:5244/api/admin/task/upload/delete?tid=<string>', 'http://localhost:5244/api/admin/task/upload/done', 'http://localhost:5244/api/admin/task/upload/retry?tid=<string>', 'http://localhost:5244/api/admin/task/upload/retry_failed', 'http://localhost:5244/api/admin/task/upload/undone', 'http://localhost:5244/api/admin/user/cancel_2fa?id=<string>', 'http://localhost:5244/api/admin/user/create', 'http://localhost:5244/api/admin/user/del_cache?username=<string>', 'http://localhost:5244/api/admin/user/delete?id=<string>', 'http://localhost:5244/api/admin/user/get?id=<string>', 'http://localhost:5244/api/admin/user/list?Page=<integer>&PerPage=<integer>', 'http://localhost:5244/api/admin/user/update', 'http://localhost:5244/api/auth/2fa/generate', 'http://localhost:5244/api/auth/2fa/verify', 'http://localhost:5244/api/auth/get_sso_id?<options>=<string>&code=<string>&method=<string>&state=<string>', 'http://localhost:5244/api/auth/login', 'http://localhost:5244/api/auth/login/hash', 'http://localhost:5244/api/auth/sso?method=<string>', 'http://localhost:5244/api/auth/sso_callback?<options>=<string>&code=<string>&method=<string>&state=<string>', 'http://localhost:5244/api/auth/sso_get_token?<options>=<string>&code=<string>&method=<string>&state=<string>', 'http://localhost:5244/api/authn/delete_authn', 'http://localhost:5244/api/authn/getcredentials', 'http://localhost:5244/api/authn/webauthn_begin_login?username=<string>', 'http://localhost:5244/api/authn/webauthn_begin_registration', 'http://localhost:5244/api/authn/webauthn_finish_login?username=<string>', 'http://localhost:5244/api/authn/webauthn_finish_registration', 'http://localhost:5244/api/fs/add_offline_download', 'http://localhost:5244/api/fs/batch_rename', 'http://localhost:5244/api/fs/copy', 'http://localhost:5244/api/fs/form', 'http://localhost:5244/api/fs/link', 'http://localhost:5244/api/fs/mkdir', 'http://localhost:5244/api/fs/move', 'http://localhost:5244/api/fs/put', 'http://localhost:5244/api/fs/recursive_move', 'http://localhost:5244/api/fs/regex_rename', 'http://localhost:5244/api/fs/remove', 'http://localhost:5244/api/fs/remove_empty_directory', 'http://localhost:5244/api/fs/rename', 'http://localhost:5244/api/me', 'http://localhost:5244/api/me/update', 'http://localhost:5244/d/<string>?sign=<string>', 'http://localhost:5244/d/<string>?sign=<string>', 'http://localhost:5244/debug/gc', 'http://localhost:5244/debug/hide_privacy', 'http://localhost:5244/debug/path/<string>?sign=<string>', 'http://localhost:5244/favicon.ico', 'http://localhost:5244/i/<string>', 'http://localhost:5244/p/<string>?sign=<string>', 'http://localhost:5244/p/<string>?sign=<string>', 'http://localhost:5244/robots.txt']}}, 'vuln_django_play_api': {200: {'count': 6, 'percentage': 66.66666666666666, 'paths': ['http://localhost:8020/', 'http://localhost:8020/admin', 'http://localhost:8020/polls', 'http://localhost:8020/polls/search', 'http://localhost:8020/polls/<string>', 'http://localhost:8020/polls/<integer>']}}, 'dvws-node': {200: {'count': 4, 'percentage': 18.181818181818183, 'paths': ['http://localhost:80/api/v1/info', 'http://localhost:80/api/v2/passphrase/<string>', 'http://localhost:80/api/v2/release/<string>', 'http://localhost:80/dvwsuserservice?wsdl=<string>']}}}
        """
        if isinstance(code, int):
            code = [code]  # Convert single integer to a list
        app_info = {app_name: app_analysis.get_status_code_info(code) for app_name, app_analysis in self.apps.items()}
        # Sorting logic here (may need to be adjusted to handle the new structure)
        return app_info

    def get_all_apps_info(self, code: Union[int, List[int]]) -> List[Dict[str, Union[str, int, float, List[str]]]]:
        """
        Example usage:
            # Get information for all apps for a specific status code
            all_apps_info_404 = app_manager.get_all_apps_info(404)
            print(all_apps_info_404)

        Example output:
            [{'app_name': 'nodejs-goof', 404: {'count': 0, 'percentage': 0.0, 'paths': []}}, {'app_name': 'javaspringvulny-api', 404: {'count': 0, 'percentage': 0.0, 'paths': []}}, {'app_name': 'govwa', 404: {'count': 0, 'percentage': 0.0, 'paths': []}}, {'app_name': 'Tiredful-API', 404: {'count': 1, 'percentage': 11.11111111111111, 'paths': ['http://localhost:8000/oauth']}}, {'app_name': 'crAPI', 404: {'count': 1, 'percentage': 4.0, 'paths': ['http://localhost:8888/identity/api/v2/user/dashboard']}}, {'app_name': 'vuln_node_express_api', 404: {'count': 0, 'percentage': 0.0, 'paths': []}}, {'app_name': 'VulnerableApp', 404: {'count': 6, 'percentage': 85.71428571428571, 'paths': ['http://localhost:80/CONTENT_DISPOSITION_STATIC_FILE_LOCATION + FrameworkConstants.SLASH + "<string>', 'http://localhost:80/allEndPoint', 'http://localhost:80/allEndPointJson', 'http://localhost:80/scanner', 'http://localhost:80/scanner/metadata', 'http://localhost:80/sitemap.xml']}}, {'app_name': 'Vulnerable-Flask-App', 404: {'count': 1, 'percentage': 7.142857142857142, 'paths': ['http://localhost:5050/login?password=<string>&username=<string>']}}, {'app_name': 'alist', 404: {'count': 0, 'percentage': 0.0, 'paths': []}}, {'app_name': 'vuln_django_play_api', 404: {'count': 1, 'percentage': 11.11111111111111, 'paths': ['http://localhost:8020/polls/<integer>/results']}}, {'app_name': 'dvws-node', 404: {'count': 1, 'percentage': 4.545454545454546, 'paths': ['http://localhost:80/api/v2/login']}}]
        """
        if isinstance(code, int):
            code = [code]  # Convert single integer to a list
        return [{'app_name': app_name, **app_analysis.get_status_code_info(code)} for app_name, app_analysis in self.apps.items()]

    def __repr__(self) -> str:
        app_names = list(self.apps.keys())
        app_names.sort()
        return f'AppManager ({len(self.apps)}): {", ".join(app_names)})'


class NewmanReport:
    VALID_CODES = [200, 400, 401, 403]
    INVALID_CODES = [404, 405, 500]
    VALID_400 = [400, 401, 403]
    INVALID_400 = [404, 405]
    # Actually, it's only skipped if the http code is empty
    SKIPPED = 'Skipped'  # Represents skipped requests

    def __init__(self, app_manager: AppManager, app_details: Dict[str, str]):
        """Initialize the NewmanReport with an AppManager and app-to-repo mapping."""
        self.app_manager = app_manager
        self.app_details = app_details

    def prepare_data_for_report(self) -> Dict:
        report_data = []
        total_valid_percentage = 0
        total_endpoints = 0
        total_valid_endpoints = 0
        total_hallucinated_endpoints = 0
        success_rates = []
        for app_name, app_analysis in self.app_manager.apps.items():
            all_status_info = app_analysis.get_all_status_code_info()

            valid_paths = [
                {**endpoint, 'code': code}
                for code in self.VALID_CODES if code in all_status_info
                for endpoint in all_status_info[code]['endpoints']
            ]
            invalid_paths = [
                {**endpoint, 'code': code}
                for code in self.INVALID_CODES if code in all_status_info
                for endpoint in all_status_info[code]['endpoints']
            ]
            valid_count = len(valid_paths)
            invalid_count = len(invalid_paths)
            total_count = sum(info['count'] for info in all_status_info.values())
            valid_400_count = sum(all_status_info[code]['count'] for code in self.VALID_400 if code in all_status_info)
            invalid_400_count = sum(all_status_info[code]['count'] for code in self.INVALID_400 if code in all_status_info)
            skipped_count = all_status_info.get(self.SKIPPED, {'count': 0})['count']
            total_valid_percentage += valid_count / total_count if total_count > 0 else 0

            # Get repository URL from the mapping
            app_details = self.app_details.get(app_name)
            if app_details is None:
                app_details = {'repo': 'Unknown', 'language': 'Unknown'}

            report_data.append({
                'Application': app_name,
                'Repository URL': app_details["repo"],
                'Language': app_details["language"],
                'Valid Paths': valid_paths,
                'Invalid Paths': invalid_paths,
                'Valid Count': valid_count,
                'Invalid Count': invalid_count,
                'Valid %': f"{(valid_count / total_count) * 100:.2f}%" if total_count > 0 else "0%",
                'Invalid %': f"{(invalid_count / total_count) * 100:.2f}%" if total_count > 0 else "0%",
                'HTTP 200 %': f"{(all_status_info.get(200, {'count': 0})['count'] / total_count) * 100:.2f}%" if total_count > 0 else "0%",
                '400 Valid %': f"{(valid_400_count / total_count) * 100:.2f}%" if total_count > 0 else "0%",
                '400 Invalid %': f"{(invalid_400_count / total_count) * 100:.2f}%" if total_count > 0 else "0%",
                'Skipped %': f"{(skipped_count / total_count) * 100:.2f}%" if total_count > 0 else "0%",
            })
            total_endpoints += len(valid_paths) + len(invalid_paths)
            total_valid_endpoints += len(valid_paths)
            total_hallucinated_endpoints += len(invalid_paths)
            success_rates.append(valid_count / total_count if total_count > 0 else 0)
        # Sort by Application name
        report_data.sort(key=lambda x: x['Application'])
        average_success_rate = sum(success_rates) / len(success_rates) if success_rates else 0
        repository_count = len(report_data)

        summary = {
            'Average Success Rate': f"{average_success_rate * 100:.2f}%",
            'Hallucinated Endpoints': total_hallucinated_endpoints,
            'Valid Endpoints': total_valid_endpoints,
            'Total Endpoints': total_endpoints,
            'Repository Count': repository_count
        }

        return {'report_data': report_data, 'summary': summary}

    def render_markdown_report(self) -> str:
        data = self.prepare_data_for_report()
        report_data = data['report_data']
        summary = data['summary']

        # Set up Jinja2 environment and load template
        template_path = dirname(__file__)
        env = Environment(loader=FileSystemLoader(template_path))
        template = env.get_template("newman_summary.md.j2")

        # Render the template with the report data
        rendered_markdown = template.render(report_data=report_data, summary=summary)
        return rendered_markdown

    def write_markdown_report(self, output_path: str) -> None:
        """
        Renders a markdown report using a Jinja2 template and writes it to a file.

        :param output_path: Path where the rendered markdown file will be saved.
        :return:
        """
        rendered_markdown = self.render_markdown_report()
        if exists(output_path):
            print(f"Removing existing report at {output_path}")
            remove(output_path)
        # Write the rendered markdown to a file
        with open(output_path, 'w') as file:
            file.write(rendered_markdown)
        print(f"Markdown report generated: {output_path}")
