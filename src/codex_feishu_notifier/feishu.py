import json

import requests


class FeishuBot:
    def __init__(self, app_id: str, app_secret: str, timeout: int = 10):
        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout
        self.tenant_access_token = None
        self.base_url = "https://open.feishu.cn"

    def _post_json(self, url: str, headers: dict, payload: dict) -> dict:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )
        try:
            data = response.json()
        except ValueError as exc:
            response.raise_for_status()
            raise RuntimeError(f"Feishu returned non-JSON content: {response.text}") from exc

        if not response.ok:
            raise RuntimeError(
                f"Feishu HTTP {response.status_code}: "
                f"{json.dumps(data, ensure_ascii=False)}"
            )

        return data

    def get_tenant_access_token(self) -> str:
        url = f"{self.base_url}/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        data = self._post_json(url, headers, payload)

        if data.get("code") != 0:
            raise RuntimeError(f"Failed to get tenant_access_token: {data}")

        self.tenant_access_token = data["tenant_access_token"]
        return self.tenant_access_token

    def check_credentials(self) -> bool:
        return bool(self.get_tenant_access_token())

    def send_text(
        self,
        receive_id: str,
        text: str,
        receive_id_type: str = "open_id",
    ) -> dict:
        if not self.tenant_access_token:
            self.get_tenant_access_token()

        url = f"{self.base_url}/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
        headers = {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8",
        }
        payload = {
            "receive_id": receive_id,
            "msg_type": "text",
            "content": json.dumps({"text": text}, ensure_ascii=False),
        }
        return self._post_json(url, headers, payload)
