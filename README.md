# SonarQube + Jenkins (Source analysis + Quality Gate)

Flow: Checkout -> Unit test + coverage -> SonarQube analysis -> Quality Gate (blocks) -> Deploy

## A. EC2 setup (once)
1. Launch EC2: Ubuntu 22.04, **t3.medium** (4 GB RAM; t2.micro will NOT run SonarQube), 20 GB disk.
2. Security group inbound: 22 (your IP), 8080 (Jenkins), 9000 (SonarQube).
3. From Windows cmd:
   ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
4. On EC2:
   git clone <your-repo-url> && cd <repo>
   bash ec2-setup/setup-ec2.sh

## B. SonarQube
1. Open http://<EC2-IP>:9000 -> login admin/admin -> change password.
2. My Account -> Security -> Generate Token (name: jenkins) -> copy it.
3. Administration -> Configuration -> Webhooks -> Create:
   Name: jenkins   URL: http://<EC2-PRIVATE-IP>:8080/sonarqube-webhook/
   (use the PRIVATE ip, not localhost - SonarQube runs in Docker)

## C. Jenkins
1. Open http://<EC2-IP>:8080, paste initial password, install suggested plugins, create admin user.
2. Manage Jenkins -> Plugins -> install **SonarQube Scanner**.
3. Manage Jenkins -> Credentials -> Global -> Add: kind *Secret text*, secret = Sonar token, ID = sonar-token.
4. Manage Jenkins -> System -> SonarQube servers -> Add:
   Name: SonarQube | URL: http://<EC2-PRIVATE-IP>:9000 | token: sonar-token
5. Manage Jenkins -> Tools -> SonarQube Scanner installations -> Add:
   Name: sonar-scanner | Install automatically (latest).
6. New Item -> Pipeline -> Pipeline script from SCM -> Git -> your repo URL, branch main, script path Jenkinsfile.

## D. Push the code (Windows cmd, in this folder)
   git init
   git add .
   git commit -m "sonar jenkins demo"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main

## E. Run and collect proof
Build 1 (PASS): Build Now -> all stages green. Screenshots:
 - Jenkins stage view (green) + Console Output (shows "Quality Gate passed")
 - SonarQube project dashboard, "Passed" badge

Build 2 (FAIL - proves code quality blocks the next stage):
   copy demo-fail\bad_code.py app\bad_code.py
   git add . && git commit -m "add bad code" && git push
 Build Now -> Quality Gate stage fails (red), Deploy stage is skipped. Screenshots:
 - Jenkins stage view with red Quality Gate and skipped Deploy
 - SonarQube dashboard "Failed" with issues (vulnerabilities, hotspots, coverage)

Then delete app\bad_code.py, push, and build again to show it recovers.

## Troubleshooting
- Pipeline hangs at Quality Gate: webhook missing/wrong URL.
- SonarQube container exits: vm.max_map_count not set or instance too small.
- "python3 -m venv" error: sudo apt-get install python3-venv
