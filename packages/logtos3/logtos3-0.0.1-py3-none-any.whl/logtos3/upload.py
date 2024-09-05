import boto3
from botocore.exceptions import NoCredentialsError, ClientError

class S3Manager:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name, s3_path, region_name="ap-northeast-2"):
        """
        S3Manager 객체 초기화

        Parameters:
        - aws_access_key_id: str, AWS 접근 키
        - aws_secret_access_key: str, AWS 비밀 접근 키
        - aws_session_token: str, AWS 세션 토큰 (필요한 경우)
        - bucket_name: str, S3 버킷 이름
        - region_name: str, AWS 리전 (기본값: us-east-1)
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.s3_path = s3_path
        self.file_content = ''

    def print(self, file_name, file_content):
        """
        S3에 파일 업로드

        Parameters:
        - file_content: str, 파일 내용
        - s3_path: str, S3에서의 파일 경로
        - file_name: str, 업로드할 파일 이름

        Returns:
        - bool: 성공 여부 (True: 성공, False: 실패)
        """
        try:
            self.file_content = self.file_content +'\n'+ file_content
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=f"{self.s3_path}{file_name}",
                Body=self.file_content
            )
            print(f"File uploaded successfully to s3://{self.bucket_name}/{self.s3_path}{file_name}")
            return file_content
        except NoCredentialsError:
            msg = "AWS Credentials are not available."
            print(msg)
            return msg
        except ClientError as e:
            msg = f"An error occurred: {e}"
            return msg
