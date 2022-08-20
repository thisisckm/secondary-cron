aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 824775819187.dkr.ecr.eu-west-2.amazonaws.com
docker build -t secondary-cron-uk-v1 .
docker tag secondary-cron-uk-v1:latest 824775819187.dkr.ecr.eu-west-2.amazonaws.com/secondary-cron-uk-v1:latest
docker push 824775819187.dkr.ecr.eu-west-2.amazonaws.com/secondary-cron-uk-v1:latest