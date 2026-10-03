import streamlit as st
import random

st.set_page_config(page_title="AWS Cloud Quest", page_icon="☁️", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #1a1b26;
        color: #ffffff;
    }
    .category-header {
        background-color: #2d3748;
        color: #f6ad55;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
        border: 1px solid #4a5568;
    }
    .stButton>button {
        background-color: #f6ad55;
        color: #1a202c;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        width: 100%;
        height: 60px;
        margin: 5px 0;
    }
    .stButton>button:hover {
        background-color: #ed8936;
    }
    .stButton>button:disabled {
        background-color: #4a5568;
        color: #a0aec0;
        text-decoration: line-through;
    }
    .question-box {
        background-color: #2d3748;
        border: 3px solid #f6ad55;
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
    }
    .question-title {
        color: #f6ad55;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .question-text {
        color: #ffffff;
        font-size: 28px;
        line-height: 1.4;
    }
    .stMetric {
        background-color: #2d3748;
        padding: 10px;
        border-radius: 10px;
    }
    .stMetric label {
        color: #ffffff !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #f6ad55 !important;
    }
    .sidebar .stMetric label {
        color: #ffffff !important;
    }
    .sidebar .stMetric [data-testid="stMetricValue"] {
        color: #f6ad55 !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #161822;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #ffffff !important;
    }
    .stMarkdown p, .stMarkdown h3 {
        color: #ffffff !important;
    }
    .game-over-container {
        text-align: center;
        padding: 40px;
    }
    .game-over-title {
        color: #f6ad55;
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .game-over-stat {
        color: #ffffff;
        font-size: 24px;
        margin: 15px 0;
    }
    .play-again-btn {
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'best_streak' not in st.session_state:
    st.session_state.best_streak = 0
if 'answered' not in st.session_state:
    st.session_state.answered = set()
if 'current_q' not in st.session_state:
    st.session_state.current_q = None
if 'selected_opt' not in st.session_state:
    st.session_state.selected_opt = None
if 'started' not in st.session_state:
    st.session_state.started = False
if 'game_ended' not in st.session_state:
    st.session_state.game_ended = False
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'result_logged' not in st.session_state:
    st.session_state.result_logged = False

questions_data = {
    "☁️ Cloud Concepts": [
        {"q": "What is the primary benefit of using AWS Availability Zones?", "opts": ["They reduce costs by sharing resources", "They provide fault tolerance by isolating failures", "They increase data transfer speed", "They automatically back up data"], "ans": 1, "exp": "AZs are physically isolated to provide high availability and fault tolerance."},
        {"q": "Which BEST describes cloud computing?", "opts": ["Installing software locally", "On-demand delivery of IT resources over the Internet with pay-as-you-go pricing", "Storing data on physical office servers", "Using a single server for all apps"], "ans": 1, "exp": "Cloud computing is on-demand delivery of IT resources over the Internet with pay-as-you-go pricing."},
        {"q": "How many Availability Zones does each AWS Region have at minimum?", "opts": ["One", "Two", "Three", "Five"], "ans": 2, "exp": "Each Region has at least three AZs for high availability."},
        {"q": "Which component is a geographic area with multiple data centers?", "opts": ["Availability Zone", "Edge Location", "Region", "VPC"], "ans": 2, "exp": "A Region is a geographic area containing multiple isolated AZs."},
        {"q": "What does 'high availability' mean in AWS?", "opts": ["Servers run at max CPU", "Systems remain operational during failures", "Data is always encrypted", "Apps load in under 1 second"], "ans": 1, "exp": "High availability means systems remain operational even when components fail."},
        {"q": "Which is NOT a benefit of cloud computing?", "opts": ["Trade capital for variable expense", "Economies of scale", "Increase time to market", "Stop guessing capacity"], "ans": 2, "exp": "Cloud computing DECREASES time to market, it does not increase it."},
        {"q": "What is an AWS Edge Location used for?", "opts": ["Running EC2 instances", "Caching content closer to users to reduce latency", "Storing database backups", "Managing IAM users"], "ans": 1, "exp": "Edge Locations cache content via CloudFront to reduce latency for end users."},
        {"q": "Difference between a Region and an AZ?", "opts": ["They are the same", "Region is a geographic area; AZ is an isolated data center within it", "AZ is larger than a Region", "Regions only exist in the US"], "ans": 1, "exp": "A Region is a geographic area containing multiple isolated AZs."},
        {"q": "What does shifting from CapEx to OpEx mean?", "opts": ["Paying a large upfront cost", "Paying for IT resources on a pay-as-you-go basis", "Leasing a physical data center", "Buying software licenses in bulk"], "ans": 1, "exp": "Cloud computing allows you to trade capital expense for variable expense."},
        {"q": "Which cloud advantage allows deploying apps in multiple regions with a few clicks?", "opts": ["Stop guessing capacity", "Increase speed and agility", "Go global in minutes", "Benefit from massive economies of scale"], "ans": 2, "exp": "With the cloud, you can deploy your application in multiple physical locations worldwide in minutes."}
    ],
    "🔒 Security & Compliance": [
        {"q": "What is the AWS Shared Responsibility Model?", "opts": ["AWS handles all security", "Customer handles all security", "AWS handles security OF the cloud; customer handles security IN the cloud", "Split 50/50"], "ans": 2, "exp": "AWS manages the cloud infrastructure; customers manage their data and apps."},
        {"q": "Which service manages user access and permissions?", "opts": ["Amazon S3", "AWS IAM", "Amazon EC2", "AWS Lambda"], "ans": 1, "exp": "IAM manages users, groups, roles, and permissions."},
        {"q": "What is the principle of least privilege?", "opts": ["Give all users admin access", "Grant only minimum permissions needed", "Never grant permissions", "Share credentials"], "ans": 1, "exp": "Grant only the permissions necessary to perform a specific task."},
        {"q": "Which service records all API calls in your account?", "opts": ["CloudWatch", "AWS CloudTrail", "AWS Config", "GuardDuty"], "ans": 1, "exp": "CloudTrail logs all API calls for auditing and compliance."},
        {"q": "What does MFA stand for?", "opts": ["Managed Firewall Access", "Multi-Factor Authentication", "Multiple File Authorization", "Main Frame Architecture"], "ans": 1, "exp": "MFA adds an extra layer of security beyond just a password."},
        {"q": "Which compliance program is specific to the US government?", "opts": ["GDPR", "HIPAA", "FedRAMP", "PCI DSS"], "ans": 2, "exp": "FedRAMP is the US government-wide cloud security authorization program."},
        {"q": "What is the purpose of AWS Artifact?", "opts": ["Deploy containers", "Access compliance reports on demand", "Monitor performance", "Manage DNS"], "ans": 1, "exp": "Artifact provides on-demand access to security and compliance reports."},
        {"q": "Which service protects against DDoS attacks?", "opts": ["AWS WAF", "AWS Shield", "Amazon Inspector", "AWS KMS"], "ans": 1, "exp": "AWS Shield provides managed DDoS protection."},
        {"q": "The AWS CAF has six perspectives. Which is NOT one?", "opts": ["Business", "People", "Technology", "Governance"], "ans": 2, "exp": "The six CAF perspectives are Business, People, Governance, Platform, Security, and Operations."},
        {"q": "What is the primary purpose of the AWS CAF?", "opts": ["List all AWS services", "Help organizations design a roadmap to successful cloud adoption", "Automatically secure your account", "Manage monthly billing"], "ans": 1, "exp": "The AWS CAF helps organizations design a roadmap to successful cloud adoption."},
        {"q": "Which service uses ML to discover and protect sensitive data?", "opts": ["Amazon Macie", "Amazon Inspector", "AWS GuardDuty", "AWS Config"], "ans": 0, "exp": "Amazon Macie uses ML to identify and protect sensitive data like PII."},
        {"q": "What is the primary function of AWS KMS?", "opts": ["Manage passwords", "Create and control cryptographic keys", "Monitor network traffic", "Scan for malware"], "ans": 1, "exp": "AWS KMS makes it easy to create and manage cryptographic keys."},
        {"q": "Which service consolidates multiple AWS accounts?", "opts": ["AWS IAM", "AWS Organizations", "AWS Control Tower", "AWS RAM"], "ans": 1, "exp": "AWS Organizations helps you centrally govern your environment."},
        {"q": "Which service provides intelligent threat detection?", "opts": ["Amazon GuardDuty", "AWS Shield", "AWS WAF", "Amazon Macie"], "ans": 0, "exp": "Amazon GuardDuty continuously monitors for malicious activity."},
        {"q": "Which privacy regulation grants EU individuals rights over their data?", "opts": ["HIPAA", "PCI DSS", "GDPR", "SOC 2"], "ans": 2, "exp": "GDPR is a comprehensive privacy law in the EU."},
        {"q": "Which service replaces hardcoded credentials with managed secrets?", "opts": ["Parameter Store", "AWS Secrets Manager", "AWS KMS", "AWS IAM"], "ans": 1, "exp": "AWS Secrets Manager protects secrets with automatic rotation."},
        {"q": "Which service provides a managed network firewall for VPC?", "opts": ["Security Groups", "Network ACLs", "AWS Network Firewall", "AWS WAF"], "ans": 2, "exp": "AWS Network Firewall deploys essential network protections for VPCs."},
        {"q": "Which service assesses EC2 instances for software vulnerabilities?", "opts": ["Amazon Inspector", "AWS Config", "Amazon GuardDuty", "Trusted Advisor"], "ans": 0, "exp": "Amazon Inspector continuously scans for software vulnerabilities."},
        {"q": "What is Data Residency?", "opts": ["Data Encryption", "Legal requirement that data is stored within a specific geographic boundary", "Data Replication", "Data Obfuscation"], "ans": 1, "exp": "Data residency refers to the requirement that data is stored within a specific country's borders."},
        {"q": "Which IAM feature identifies resources shared with an external entity?", "opts": ["IAM Access Analyzer", "IAM Credential Report", "IAM Policy Simulator", "AWS Organizations SCPs"], "ans": 0, "exp": "IAM Access Analyzer helps identify resources shared externally."}
    ],
    "⚙️ Technology": [
        {"q": "Which service provides virtual servers?", "opts": ["Amazon S3", "Amazon EC2", "Amazon RDS", "AWS Lambda"], "ans": 1, "exp": "EC2 provides resizable virtual servers."},
        {"q": "Which is AWS's object storage service?", "opts": ["Amazon EBS", "Amazon S3", "Amazon RDS", "Amazon EFS"], "ans": 1, "exp": "S3 provides scalable object storage."},
        {"q": "What is serverless computing?", "opts": ["No servers exist", "Run code without managing servers, pay only for compute time", "Use physical office servers", "Rent a dedicated server"], "ans": 1, "exp": "Serverless runs code without provisioning servers."},
        {"q": "Which is a managed relational database service?", "opts": ["DynamoDB", "Amazon RDS", "Redshift", "ElastiCache"], "ans": 1, "exp": "RDS makes it easy to set up and scale relational databases."},
        {"q": "Difference between S3 and EBS?", "opts": ["Same service", "S3 is object storage; EBS is block storage for EC2", "EBS is object; S3 is block", "S3 is for images only"], "ans": 1, "exp": "S3 is object storage via API; EBS is block storage attached to EC2."},
        {"q": "Which service distributes incoming traffic?", "opts": ["Route 53", "Elastic Load Balancing", "Auto Scaling", "CloudFront"], "ans": 1, "exp": "ELB distributes traffic across multiple targets."},
        {"q": "What does Amazon VPC allow?", "opts": ["Send emails", "Create an isolated virtual network", "Host static sites", "Train ML models"], "ans": 1, "exp": "VPC lets you provision a logically isolated section of the AWS Cloud."},
        {"q": "Which service provides a NoSQL database?", "opts": ["RDS", "Aurora", "Amazon DynamoDB", "Neptune"], "ans": 2, "exp": "DynamoDB is a fully managed, fast NoSQL database service."},
        {"q": "Which service deploys apps without worrying about infrastructure?", "opts": ["Amazon EC2", "AWS Elastic Beanstalk", "Amazon S3", "AWS Lambda"], "ans": 1, "exp": "Elastic Beanstalk handles deployment and infrastructure."},
        {"q": "Which VPC component allows private instances outbound internet access?", "opts": ["Internet Gateway", "NAT Gateway", "VPC Peering", "AWS Direct Connect"], "ans": 1, "exp": "A NAT Gateway allows private instances to connect out."},
        {"q": "Which S3 class is for long-term archiving?", "opts": ["S3 Standard", "S3 Intelligent-Tiering", "S3 Glacier Flexible Retrieval", "S3 One Zone-IA"], "ans": 2, "exp": "S3 Glacier is for low-cost archiving."},
        {"q": "Which database is multi-region and 5x faster than standard MySQL?", "opts": ["DynamoDB", "RDS for MySQL", "Amazon Aurora", "Redshift"], "ans": 2, "exp": "Amazon Aurora is built for the cloud with high performance."},
        {"q": "Which AWS service is used to register domain names and route end-user requests?", "opts": ["AWS Direct Connect", "Amazon Route 53", "Amazon CloudFront", "AWS Global Accelerator"], "ans": 1, "exp": "Amazon Route 53 is a highly available and scalable cloud DNS web service."},
        {"q": "Which AWS service is a fully managed data warehouse for analyzing large datasets using SQL?", "opts": ["Amazon RDS", "Amazon DynamoDB", "Amazon Redshift", "Amazon Athena"], "ans": 2, "exp": "Amazon Redshift is a fast, fully managed data warehouse."},
        {"q": "Which AWS messaging service uses a pull-based queue model for decoupling microservices?", "opts": ["Amazon SNS", "Amazon SQS", "Amazon SES", "Amazon Pinpoint"], "ans": 1, "exp": "Amazon SQS is a fully managed message queuing service."},
        {"q": "What are the six pillars of the AWS Well-Architected Framework?", "opts": ["Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability", "Security, Reliability, Performance, Cost, Networking, Storage", "High Availability, Fault Tolerance, Disaster Recovery, Security, Cost, Performance", "Compute, Storage, Database, Networking, Security, Management"], "ans": 0, "exp": "These six pillars provide the framework for secure, high-performing infrastructure."},
        {"q": "Which AWS service allows you to run queries on data directly in Amazon S3 using SQL?", "opts": ["Amazon Redshift", "Amazon Athena", "Amazon QuickSight", "AWS Glue"], "ans": 1, "exp": "Amazon Athena is an interactive query service for S3."},
        {"q": "Which AWS service allows you to run containers without managing EC2 instances?", "opts": ["Amazon ECS with Fargate", "AWS Elastic Beanstalk", "Amazon EKS", "AWS Batch"], "ans": 0, "exp": "AWS Fargate is a serverless compute engine for containers."},
        {"q": "Which AWS service provides a dedicated, private network connection between on-premises and AWS?", "opts": ["AWS VPN", "Amazon VPC Peering", "AWS Direct Connect", "Amazon CloudFront"], "ans": 2, "exp": "AWS Direct Connect links your internal network to AWS over a standard Ethernet fiber-optic cable."},
        {"q": "Which AWS service is a BI tool for creating interactive dashboards and visualizations?", "opts": ["Amazon QuickSight", "Amazon CloudWatch", "AWS CloudTrail", "Amazon Inspector"], "ans": 0, "exp": "Amazon QuickSight is a cloud-scale business intelligence service."},
        {"q": "Which AWS service helps coordinate multiple AWS services into serverless workflows?", "opts": ["AWS Lambda", "Amazon EventBridge", "AWS Step Functions", "Amazon SNS"], "ans": 2, "exp": "AWS Step Functions lets you coordinate multiple AWS services into serverless workflows."},
        {"q": "Which AWS service enables you to add user sign-up, sign-in, and access control to apps?", "opts": ["AWS IAM", "Amazon Cognito", "AWS Directory Service", "Amazon GuardDuty"], "ans": 1, "exp": "Amazon Cognito lets you add user sign-up, sign-in, and access control quickly."}
    ],
    "💰 Billing & Pricing": [
        {"q": "Pay for compute by the hour with no commitment?", "opts": ["Reserved", "On-Demand", "Spot", "Dedicated Hosts"], "ans": 1, "exp": "On-Demand lets you pay by the hour/second with no commitment."},
        {"q": "Tool to visualize and analyze AWS costs?", "opts": ["CloudTrail", "AWS Cost Explorer", "CloudWatch", "Config"], "ans": 1, "exp": "Cost Explorer helps you visualize and manage costs."},
        {"q": "What is the AWS Free Tier?", "opts": ["Unlimited free resources", "Free services for 12 months + always-free offers", "Student discount only", "30-day trial"], "ans": 1, "exp": "Includes 12-month free trials and always-free offers."},
        {"q": "What are Spot Instances?", "opts": ["Reserved for 1-3 years", "Spare capacity at up to 90% discount, can be interrupted", "Dedicated servers", "Free testing instances"], "ans": 1, "exp": "Spot Instances use spare capacity at steep discounts."},
        {"q": "Which support plan is free?", "opts": ["Developer", "Business", "Enterprise", "Basic"], "ans": 3, "exp": "Basic support is free."},
        {"q": "What is AWS Budgets used for?", "opts": ["Deploy apps", "Set cost/usage budgets with alerts", "Manage IAM", "Monitor health"], "ans": 1, "exp": "Budgets alert you when costs exceed thresholds."},
        {"q": "What is the AWS Pricing Calculator?", "opts": ["Reduces your bill", "Web tool to estimate service costs", "Billing dashboard", "Coupon generator"], "ans": 1, "exp": "Helps you estimate costs before building."},
        {"q": "Which model offers the highest discount for steady-state workloads?", "opts": ["On-Demand", "Spot Instances", "Savings Plans / Reserved Instances", "Dedicated Hosts"], "ans": 2, "exp": "Savings Plans offer up to 72% discount for 1-3 year commitments."},
        {"q": "How do you change the default AWS Region in the Console?", "opts": ["Go to Billing Dashboard", "Click Region selector in top right corner", "Contact AWS Support", "Modify IAM settings"], "ans": 1, "exp": "You can change your active Region via the dropdown in the top right."},
        {"q": "Which console feature provides real-time guidance for best practices?", "opts": ["AWS CloudTrail", "AWS Config", "AWS Trusted Advisor", "Amazon Inspector"], "ans": 2, "exp": "Trusted Advisor recommends ways to save money and improve security."}
    ]
}

for cat, qs in questions_data.items():
    for idx, q in enumerate(qs):
        q['pts'] = ((idx % 10) + 1) * 100

if not st.session_state.started:
    st.title("☁️ AWS Cloud Quest")
    st.markdown("### Welcome to your ultimate AWS Cloud Practitioner study game!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80", caption="Cloud Computing Network", use_container_width=True)
    with col2:
        st.image("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&q=80", caption="AWS Infrastructure", use_container_width=True)
    with col3:
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80", caption="Game Dashboard", use_container_width=True)
        
    st.markdown("---")
    if st.button("🚀 START GAME", use_container_width=True, type="primary"):
        st.session_state.started = True
        st.rerun()
    st.stop()

with st.sidebar:
    st.title("📊 Game Stats")
    st.metric("Current Score", f"⭐ {st.session_state.score}")
    st.metric("Current Streak", f"🔥 {st.session_state.streak}")
    st.metric("Best Streak", f" {st.session_state.best_streak}")
    
    total_qs = sum(len(v) for v in questions_data.values())
    answered_qs = len(st.session_state.answered)
    st.metric("Questions Answered", f"{answered_qs} / {total_qs}")
    
    st.markdown("---")
    st.subheader("📖 How to Play")
    st.write("1. Select a **category** and **point value**.")
    st.write("2. Read the question and choose an answer.")
    st.write("3. Click **Submit** to see if you're correct.")
    st.write("4. Build your streak and aim for the highest score!")
    
    st.markdown("---")
    if st.button("🏁 End Game", use_container_width=True):
        st.session_state.game_ended = True
        st.rerun()
        
    if st.button("🔄 Reset Game", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key not in ['started']:
                del st.session_state[key]
        st.rerun()

if st.session_state.game_ended:
    st.markdown("""
    <div class="game-over-container">
        <div class="game-over-title">🏆 Game Over!</div>
        <div class="game-over-stat">Final Score: """ + str(st.session_state.score) + """ points</div>
        <div class="game-over-stat">Best Streak: """ + str(st.session_state.best_streak) + """</div>
        <div class="game-over-stat">Questions Answered: """ + str(len(st.session_state.answered)) + """ / """ + str(sum(len(v) for v in questions_data.values())) + """</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Play Again", use_container_width=True, type="primary"):
            for key in list(st.session_state.keys()):
                if key not in ['started']:
                    del st.session_state[key]
            st.rerun()
    st.stop()

if st.session_state.current_q is None:
    st.title("☁️ AWS Cloud Quest Board")
    st.markdown("### Select a category and point value to begin! All 62 questions are available below.")
    
    cols = st.columns(4)
    point_values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    
    for i, cat in enumerate(questions_data.keys()):
        with cols[i]:
            st.markdown(f'<div class="category-header">{cat}</div>', unsafe_allow_html=True)
            
            for pts in point_values:
                available_indices = [
                    idx for idx, q in enumerate(questions_data[cat]) 
                    if q['pts'] == pts and (cat, idx) not in st.session_state.answered
                ]
                
                count = len(available_indices)
                
                if count > 0:
                    btn_label = f"⭐ {pts} pts (x{count})"
                    if st.button(btn_label, key=f"btn_{cat}_{pts}"):
                        chosen_idx = random.choice(available_indices)
                        st.session_state.current_q = (cat, chosen_idx)
                        st.session_state.selected_opt = None
                        st.session_state.submitted = False
                        st.session_state.result_logged = False
                        st.rerun()
                else:
                    st.button(f"✅ {pts} pts", disabled=True, key=f"btn_{cat}_{pts}_done")

else:
    cat, q_idx = st.session_state.current_q
    q = questions_data[cat][q_idx]
    points = q['pts']
    
    st.markdown(f"""
    <div class="question-box">
        <div class="question-title">📝 Question ({points} points)</div>
        <div class="question-text">{q['q']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Choose your answer:")
    
    cols = st.columns(2)
    for i, opt in enumerate(q['opts']):
        with cols[i % 2]:
            btn_label = f"🟠 {opt}" if st.session_state.selected_opt == opt else f"🔵 {opt}"
                
            if st.button(btn_label, key=f"opt_{q_idx}_{i}", use_container_width=True):
                st.session_state.selected_opt = opt
                st.session_state.submitted = False
                st.session_state.result_logged = False
                st.rerun()
                
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("✅ Submit Answer", key="submit_btn", use_container_width=True):
        if st.session_state.selected_opt is None:
            st.warning("Please select an answer first!")
        else:
            st.session_state.submitted = True
            st.session_state.result_logged = False
            st.rerun()
                
    if st.session_state.submitted:
        if not st.session_state.result_logged:
            correct_idx = q['ans']
            correct_opt = q['opts'][correct_idx]
            
            if st.session_state.selected_opt == correct_opt:
                st.success(f"✅ Correct! You earned {points} points.")
                st.session_state.score += points
                st.session_state.streak += 1
                if st.session_state.streak > st.session_state.best_streak:
                    st.session_state.best_streak = st.session_state.streak
            else:
                st.error(f"❌ Incorrect. The correct answer is: **{correct_opt}**")
                st.session_state.streak = 0
                
            st.info(f"💡 **Explanation:** {q['exp']}")
            
            st.session_state.answered.add((cat, q_idx))
            st.session_state.result_logged = True
        else:
            correct_idx = q['ans']
            correct_opt = q['opts'][correct_idx]
            if st.session_state.selected_opt == correct_opt:
                st.success(f"✅ Correct! You earned {points} points.")
            else:
                st.error(f"❌ Incorrect. The correct answer is: **{correct_opt}**")
            st.info(f"💡 **Explanation:** {q['exp']}")
        
        if st.button("➡️ Back to Board", key="back_btn", use_container_width=True):
            st.session_state.current_q = None
            st.session_state.selected_opt = None
            st.session_state.submitted = False
            st.session_state.result_logged = False
            st.rerun()