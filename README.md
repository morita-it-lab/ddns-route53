
How to Use
----------
1. Create an IAM role that can manage Route53 and obtain the access key.
2. Describe the settings in the `.env` file.
3. Run `docker compose up -d` to start the container.

AWS Policy Examples
----------

Please replace ABCD1234567890 with the appropriate hosted zone ID.

```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": [
				"route53:ChangeResourceRecordSets",
				"route53:GetChange"
			],
			"Resource": [
				"arn:aws:route53:::change/ABCD1234567890",
				"arn:aws:route53:::hostedzone/ABCD1234567890"
			]
		}
	]
}
```

Note
----------
- By using `DISCORD_WEBHOOK_URL`, you can send a notification to Discord when the IP address is updated.