Cucumber HTML Report Duration Parser
===

Background
====

Nowadays, we build our CI/CD in the cloud platform. It is very common for us to build cucumber testing
parallel to decrease the testing time and improve the efficiency.
For example, in my project, I split the cucumber cases to multiple groups. Every group does testing
against separate instant created apps. One pipeline can control the whole process, based on some parameters you specify to build apps, deploy them then do testings in parallel.

One important thing is how to split the cucumber cases to reasonable groups.
The parser is to resolve the problem.

How it works
===
Shortly, we parser the 'overview-features.html' cucumber report to get the duration and features map, then based on the threshold user specifies, the parser would group the features automatically.
For example, ideally, if all cases run in 300 seconds, we specify the threshold as 100, the parser
would split them to 3 groups. The duration of each group is close to 100.

How to use it
===
Python 3 and some basic python libs(you can see the file directly to confirm the packages) are needed. And you need to download your 'overview-features.html' cucumber report from your Jen`kins project, then try to run the following command:
```
python3 cucumber_feature_duration_parser.py --cucumber-html-report=overview-features.html
--threshold=900
```
You will get the following output:
```
[features_time_parser.py::format_features_groups] INFO Complete: format the grouped features as below:
{' -n "A light weight empty module push e2e case" -n "A simple example E2E test case" -n "Add "Product Security Reviewer" field" -n "Add ability to bulk remove builds in an advisory" -n "Add bug to advisory" -n "Add mixed types of builds in one same advisory" -n "Attach multi-arch container builds to advisories" -n "Batch" -n "Blacklist subpackages from RHN" -n "Brew" -n "Bug advisory eligibility" -n "CAT" -n "CDN Docker Push"': 1071, ' -n "Calculate \'reboot_suggested\' value based on packages" -n "Container Health Index Grade" -n "Edit advisory" -n "Embargoed Advisory dependency" -n "Errata and Bugzilla interactions" -n "Login" -n "Main stream release for RHEL product versions and variants" -n "Module builds on builds tab" -n "Multi-Product" -n "Older build and newer build of same package" -n "Product Listing features" -n "Product Listings" -n "Product Security Approval" -n "Provide option to 
disable ACL (Approved Component List) requirement for releases" -n "Publish all erratum changes to UMB"': 1036, ' -n "Push multiple advisories in a batch" -n "RHSAs require a CPE" -n "RPM files should be shown on content page for RHEL-8 advisory" -n "RPM manifest in Container" -n "RPMDiff support for module builds" -n "Released build validation" -n "The policy for role buildroot" -n "The rule of setting released build" -n "bug eligibility checks for rhel8 bugs"': 811}
```
One key is one feature group.

Free to enjoy it!
