# Alexa Set The Mood
This is a side project to set the mood using my Alexa.

## Setting up your Lambda Function
1. Log into the [AWS management Console](https://aws.amazon.com/). Create an account if you need to.
2. From the list of services, select Lambda
3. Set your region to **US East (N. Virginia)**
4. Choose Create a Lambda Function
5. In the search filter box, type Alexa
6. Select blueprint **alexa-skills-kit-color-expert-python**
7. Name your function. I call mine logWeight
8. Under Lambda function handler and role, select **Create a custom role**.
9. When the IAM role management console opens, choose **Allow** to go back to the previous Lambda console.
10. The role should read `lambda_basic_execution`.
11. In your [IAM roles](https://console.aws.amazon.com/iam/home#/roles) attach the **AWSLambdaFullAccess** policy to your role.
12. Add environment variables. These give you access to Spotify. Note that the Alexa application id and the Alexa test application id are filtered.
    1. **SPOTIPY_CLIENT_ID**
    2. **SPOTIPY_CLIENT_SECRET**
    3. **SPOTIPY_REDIRECT_URI**
    4. **SPOTIPY_SCOPE**
    5. **SPOTIPY_TOKEN_INFO**
    6. **ALEXA_APPLICATION_ID**
    7. **ALEXA_TEST_APPLICATION_ID**
    8. **SPOTIPY_DEVICE_ID**
    9. **SPOTIPY_CONTEXT_URI**
    10. **IFTTT_URI**

## Setting up your Amazon developer portal
1. Sign into the [Amazon Developer Portal](https://developer.amazon.com/login.html).
2. Select Alexa
3. Under **Alexa Skills Kit**, choose **Get Started**
4. Choose **Add a New Skill**
5. Name your skill. It doesn’t really matter what it is.
6. Create an invocation name. I set it to "set the mood" Note that there are [limits](https://developer.amazon.com/docs/custom-skills/choose-the-invocation-name-for-a-custom-skill.html) to how you can invoke this skill. For example, you cannot (unfortunately) say “Alexa, I weigh 165 pounds”.
7. Choose Next
8. In the Intent Schema box, paste the following JSON code
```JSON
{
  "intents": [
    {
      "intent": "SetTheMood"
    },
    {
      "intent": "AMAZON.HelpIntent"
    }
  ]
}
```
10. Under the Sample Utterances enter
```
SetTheMood set the mood
```
12. Choose Next
13. Select the Endpoint **AWS Lambda ARN** then paste your ARN code from step 1-14. Select **North America** as your region, and for **Account Linking** select **No**, then choose **Next**.

## Uploading the code
1. AWS Lambda requires all python packages to be at the root file level.
2. While within the project directory you can call `./install.sh` to install all of the requirements.
3. Zip up all of the files by running `zip -r -X lambdaD.zip .`
4. Then upload the zipfile to your lambda function

## Resources and Credit
- https://developer.amazon.com/alexa-skills-kit/alexa-skill-quick-start-tutorial
- https://github.com/jryoo/spotipy
- https://github.com/plamere/spotipy