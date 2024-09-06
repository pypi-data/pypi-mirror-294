from os.path import join, dirname
import unittest

from api_validator.tools.oasdiff import OasdiffOutput
from api_validator.diff_utils.job_summary import GitHubJobSummary


class TestOasdiffOutput(unittest.TestCase):
    def setUp(self):
        self.jellyfin_file = join(dirname(__file__), "oasdiff_files", "jellyfin.yml")
        self.jellyfin_revision = join(dirname(__file__), "oasdiff_files", "jellyfin-revision.yml")
        self.javaspringvulny_file = join(dirname(__file__), "oasdiff_files", "javaspringvulny.yml")
        self.javaspringvulny_revision = join(dirname(__file__), "oasdiff_files", "javaspringvulny-revision.yml")
        self.crapi_file = join(dirname(__file__), "oasdiff_files", "crAPI.yml")
        self.crapi_revision = join(dirname(__file__), "oasdiff_files", "crAPI-spring-revision.yml")
        self.dvws_node_file = join(dirname(__file__), "oasdiff_files", "dvws-node.yml")
        self.dvws_node_revision = join(dirname(__file__), "oasdiff_files", "dvws-node-revision.yml")
        self.cert_viewer_revision = join(dirname(__file__), "oasdiff_files", "cert-viewer-revision.yml")
        self.cert_viewer_oasdiff = join(dirname(__file__), "oasdiff_files", "cert-viewer-revision.yml")
        self.apereo_cas_oasdiff = join(dirname(__file__), "oasdiff_files", "apereo-cas-oasdiff.yml")

        self.cert_viewer_diff = OasdiffOutput.from_yaml(
            self.cert_viewer_oasdiff,
            repository_url="https://github.com/api-extraction-examples/cert-viewer",
            provided_swagger_file="https://raw.githubusercontent.com/api-extraction-examples/existing-openapi-specs/main/flask/flask-1.0/cert-viewer.yaml",
            new_swagger_file=self.cert_viewer_revision,
            language="python",
            elapsed_time=20.0,
        )

    def test_oasdiff_jellyfin(self):
        jellyfin_diff = OasdiffOutput.from_yaml(
            self.jellyfin_file,
            repository_url="https://github.com/NightVisionExamples/jellyfin",
            new_swagger_file=self.jellyfin_revision,
            provided_swagger_file="https://gist.githubusercontent.com/kmcquade/be7a19b5ee320a11e81078758c171261/raw/de00375dd246de6aa5a7c2bbf9b9423de7fda1e2/jellyfin-openapi-stable.json",
            language="dotnet",
            elapsed_time=20.0,
        )
        job_summary = GitHubJobSummary([jellyfin_diff], overall_elapsed_time=60)
        step_summary = job_summary.github_step_summary()
        # Some simple assertions to make sure that the output is rendered.
        self.assertTrue(
            "The API Extractor performed scans on **1** repositories to discover API endpoints" in step_summary
        )
        self.assertTrue("**Average success rate**: 96.98%" in step_summary)

    def test_oasdiff_javaspringvulny(self):
        javaspringvulny_diff = OasdiffOutput.from_yaml(
            self.javaspringvulny_file,
            repository_url="https://github.com/vulnerable-apps/javaspringvulny",
            provided_swagger_file="https://raw.githubusercontent.com/vulnerable-apps/javaspringvulny/main/openapi.yaml",
            new_swagger_file=self.javaspringvulny_revision,
            language="spring",
            elapsed_time=20.0,
        )
        paths = javaspringvulny_diff.paths
        added_paths = paths.added
        added_paths.sort()
        expected_added_paths = [
            "/",
            "/admin",
            "/admin/companies",
            "/admin/payload/stream/{size}",
            "/admin/payload/{size}",
            "/admin/payloads",
            "/admin/search",
            "/admin/users",
            "/basic-auth",
            "/hidden",
            "/hidden/cypress",
            "/hidden/hidden2",
            "/hidden/playwright",
            "/hidden/selenium",
            "/jwt-auth",
            "/log4j",
            "/login",
            "/login-code",
            "/login-form-multi",
            "/login-multi-check",
            "/payload/stream/{size}",
            "/payload/{size}",
            "/payloads",
            "/search",
            "/token-auth"
        ]
        # Future-proof - we always expect the same paths to be added
        for path in added_paths:
            self.assertIn(path, expected_added_paths)
        expected_modified_paths = [
            "/api/basic/items/search/",
            "/api/basic/items/search/{text}",
            "/api/jwt/auth/signin",
            "/api/jwt/items/search",
            "/api/jwt/items/search/",
            "/api/jwt/items/search/{text}",
            "/api/jwt/users/search/",
            "/api/jwt/users/search/bad/{text}",
            "/api/jwt/users/search/{text}",
            "/api/token/items/search/",
            "/api/token/items/search/{text}"
        ]
        modified_paths = list(paths.modified.keys())
        modified_paths.sort()
        for path in modified_paths:
            self.assertIn(path, expected_modified_paths)

    def test_oasdiff_crapi(self):
        crapi_diff = OasdiffOutput.from_yaml(
            self.crapi_file,
            repository_url="https://github.com/vulnerable-apps/crAPI",
            provided_swagger_file="https://raw.githubusercontent.com/vulnerable-apps/crAPI/develop/openapi-spec/openapi-spec.json",
            new_swagger_file=self.crapi_revision,
            language="spring",
            elapsed_time=20.0,
        )
        paths = crapi_diff.paths
        added_paths = paths.added
        added_paths.sort()
        expected = [
          "/identity/api/auth/jwks.json",
          "/identity/api/auth/verify",
          "/identity/health_check"
        ]
        for path in added_paths:
            self.assertIn(path, expected)
        modified_paths = list(paths.modified.keys())
        modified_paths.sort()
        expected = [
          "/identity/api/auth/forget-password",
          "/identity/api/auth/login",
          "/identity/api/auth/signup",
          "/identity/api/auth/v2.7/user/login-with-token",
          "/identity/api/auth/v2/check-otp",
          "/identity/api/auth/v3/check-otp",
          "/identity/api/auth/v4.0/user/login-with-token",
          "/identity/api/v2/admin/videos/{video_id}",
          "/identity/api/v2/user/change-email",
          "/identity/api/v2/user/dashboard",
          "/identity/api/v2/user/pictures",
          "/identity/api/v2/user/reset-password",
          "/identity/api/v2/user/verify-email-token",
          "/identity/api/v2/user/videos",
          "/identity/api/v2/user/videos/convert_video",
          "/identity/api/v2/user/videos/{video_id}",
          "/identity/api/v2/vehicle/add_vehicle",
          "/identity/api/v2/vehicle/resend_email",
          "/identity/api/v2/vehicle/vehicles",
          "/identity/api/v2/vehicle/{vehicleId}/location"
        ]
        for path in modified_paths:
            self.assertIn(path, expected)
        self.assertListEqual(modified_paths, expected)

    def test_dvws_node(self):
        dvws_node_diff = OasdiffOutput.from_yaml(
            self.dvws_node_file,
            repository_url="https://github.com/vulnerable-apps/dvws-node",
            provided_swagger_file="https://gist.githubusercontent.com/kmcquade/a98dfc542d07b6a385aeee0b151fd017/raw/9fc972d2ce1a76370cc1ac2f28b0fb992e29f000/dvws-node-swagger.json",
            new_swagger_file=self.dvws_node_revision,
            language="js",
            elapsed_time=20.0,
        )
        self.assertEqual(len(dvws_node_diff.paths.added), 0)
        self.assertEqual(len(dvws_node_diff.paths.modified), 0)
        self.assertEqual(dvws_node_diff.paths.deleted, None)

    def test_apereo_cas_exclusions(self):
        apereo_cas_diff = OasdiffOutput.from_yaml(
            self.apereo_cas_oasdiff,
            repository_url="https://github.com/api-extraction-examples/cas",
            provided_swagger_file="https://raw.githubusercontent.com/api-extraction-examples/existing-openapi-specs/main/spring/spring-boot-3.2/cas-web-app.json",
            language="spring",
            github_stars=10400,
            exclude_paths=["/actuator/*"],
        )
        print(apereo_cas_diff.paths.added)
        self.assertNotIn("/actuator", str(apereo_cas_diff.paths.added), "The string actuator should not appear in the added paths for apereo-cas test case.")
        print(apereo_cas_diff.paths.modified)
        self.assertNotIn("/actuator", str(apereo_cas_diff.paths.modified), "The string actuator should not appear in the added paths for apereo-cas test case.")
        print(apereo_cas_diff.paths.deleted)
        self.assertNotIn("/actuator", str(apereo_cas_diff.paths.deleted), "The string actuator should not appear in the added paths for apereo-cas test case.")

    def test_github_job_summary(self):
        jellyfin_diff = OasdiffOutput.from_yaml(
            self.jellyfin_file,
            repository_url="https://github.com/NightVisionExamples/jellyfin",
            new_swagger_file=self.jellyfin_revision,
            provided_swagger_file="https://gist.githubusercontent.com/kmcquade/be7a19b5ee320a11e81078758c171261/raw/de00375dd246de6aa5a7c2bbf9b9423de7fda1e2/jellyfin-openapi-stable.json",
            language="dotnet",
            elapsed_time=20.0,
        )
        javaspringvulny_diff = OasdiffOutput.from_yaml(
            self.javaspringvulny_file,
            repository_url="https://github.com/vulnerable-apps/javaspringvulny",
            provided_swagger_file="https://raw.githubusercontent.com/vulnerable-apps/javaspringvulny/main/openapi.yaml",
            new_swagger_file=self.javaspringvulny_revision,
            language="spring",
            elapsed_time=20.0,
        )
        crapi_diff = OasdiffOutput.from_yaml(
            self.crapi_file,
            repository_url="https://github.com/vulnerable-apps/crAPI",
            provided_swagger_file="https://raw.githubusercontent.com/vulnerable-apps/crAPI/develop/openapi-spec/openapi-spec.json",
            new_swagger_file=self.crapi_revision,
            language="spring",
            elapsed_time=20.0,
        )
        dvws_node_diff = OasdiffOutput.from_yaml(
            self.dvws_node_file,
            repository_url="https://github.com/vulnerable-apps/dvws-node",
            provided_swagger_file="https://gist.githubusercontent.com/kmcquade/a98dfc542d07b6a385aeee0b151fd017/raw/9fc972d2ce1a76370cc1ac2f28b0fb992e29f000/dvws-node-swagger.json",
            new_swagger_file=self.dvws_node_revision,
            language="js",
            elapsed_time=20.0,
        )
        outputs = [
            jellyfin_diff,
            javaspringvulny_diff,
            crapi_diff,
            dvws_node_diff,
        ]
        job_summary = GitHubJobSummary(outputs, overall_elapsed_time=60)
        step_summary = job_summary.github_step_summary()
        # Some simple assertions to make sure that the output is rendered with expected output
        self.assertTrue("**Execution Time**: The API Extraction process took 1 minutes and 20 seconds to run" in step_summary)

    def test_unmodified_endpoints(self):
        unmodified_endpoints = self.cert_viewer_diff.unmodified_endpoints()
        all_revision_endpoints = self.cert_viewer_diff.all_revision_endpoints()
        self.assertDictEqual(unmodified_endpoints[0], {'method': 'GET', 'path': '/', 'parameters': []})
        self.assertEqual(len(unmodified_endpoints), 33)
        self.assertEqual(len(all_revision_endpoints), 33)
