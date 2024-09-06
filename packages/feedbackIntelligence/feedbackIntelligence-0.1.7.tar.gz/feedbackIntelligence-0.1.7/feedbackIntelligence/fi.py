import httpx
from typing import Optional, List, Dict
from feedbackIntelligence.schemas import Message


class FeedbackIntelligenceSDK:
    def __init__(self, api_key: str):
        """
        Initialize the SDK with the base URL of the API and an optional API key for authentication.

        :param api_key: Optional API key for authentication.
        """
        self.__base_url = "https://data.feedbackintelligence.ai"
        self.__headers = {
            'Content-Type': 'application/json',
        }
        if api_key:
            self.__headers['Authorization'] = f'Bearer {api_key}'

    def add_context(self, project_id: int, context: str, context_id: Optional[int] = None) -> Dict:
        """
        Add context to the database for later use in user messages (synchronous).

        :param  project_id: The ID of the project to which the context belongs.
        :param context: The context to add.
        :param context_id: Optional context ID.
        :return: Response from the API.
        """
        url = f"{self.__base_url}/data/{project_id}/context/add"
        payload = {"context": context}
        if context_id is not None:
            payload["id"] = context_id

        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=self.__headers)
            response.raise_for_status()
            return response.json()

    async def add_context_async(self, project_id: int, context: str, context_id: Optional[int] = None) -> Dict:
        """
        Add context to the database for later use in user messages (asynchronous).

        :param  project_id: The ID of the project to which the context belongs.
        :param context: The context to add.
        :param context_id: Optional context ID.
        :return: Response from the API.
        """
        url = f"{self.__base_url}/data/{project_id}/context/add"
        payload = {"context": context}
        if context_id is not None:
            payload["id"] = context_id

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.__headers)
            response.raise_for_status()
            return response.json()

    def add_chat(self, project_id: int, chat_id: int, messages: List[Message], user_id: Optional[int] = None,
                 version: Optional[str] = None) -> Dict:
        """
        Add chat data to the database (synchronous).

        :param  project_id: The ID of the project to which the chat data belongs.
        :param chat_id: The unique ID of the chat.
        :param messages: A list of messages in the chat.
        :param user_id: Optional ID of the user who initiated the chat.
        :param version: Optional version of the chat.
        :return: Response from the API.
        """
        url = f"{self.__base_url}/data/{project_id}/chat/add"
        payload = {
            "chat_id": chat_id,
            "messages": [message.to_dict() for message in messages],
        }
        if user_id is not None:
            payload["user_id"] = user_id
        if version:
            payload["version"] = version

        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=self.__headers)
            response.raise_for_status()
            return response.json()

    async def add_chat_async(self, project_id: int, chat_id: int, messages: List[Message],
                             user_id: Optional[int] = None,
                             version: Optional[str] = "1.0") -> Dict:
        """
        Add chat data to the database (asynchronous).

        :param  project_id: The ID of the project to which the chat data belongs.
        :param chat_id: The unique ID of the chat.
        :param messages: A list of messages in the chat.
        :param user_id: Optional ID of the user who initiated the chat.
        :param version: Optional version of the chat.
        :return: Response from the API.
        """
        url = f"{self.__base_url}/data/{project_id}/chat/add"
        payload = {
            "chat_id": chat_id,
            "messages": [message.to_dict() for message in messages],
        }
        if user_id is not None:
            payload["user_id"] = user_id
        if version:
            payload["version"] = version

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.__headers)
            response.raise_for_status()
            print('done!')
            return response.json()

    def add_feedback(self, project_id: int, message: str, source: str, user_id: Optional[int] = None,
                     chat_id: Optional[int] = None, date: Optional[str] = None) -> Dict:
        """
        Add feedback data to the database (synchronous).

        :param  project_id: The ID of the project to which the feedback data belongs.
        :param message: The content of the feedback.
        :param source: The source of the feedback.
        :param user_id: Optional ID of the user who provided the feedback.
        :param chat_id: Optional ID of the chat associated with the feedback.
        :param date: Optional date the feedback was given.
        :return: Response from the API.
        """
        url = f"{self.__base_url}/data/{project_id}/feedback/add"
        payload = {
            "message": message,
            "source": source,
        }
        if user_id is not None:
            payload["user_id"] = user_id
        if chat_id is not None:
            payload["chat_id"] = chat_id
        if date:
            payload["date"] = date

        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=self.__headers)
            response.raise_for_status()
            return response.json()

    async def add_feedback_async(self, project_id: int, message: str, source: str, user_id: Optional[int] = None,
                                 chat_id: Optional[int] = None, date: Optional[str] = None) -> Dict:
        """
        Add feedback data to the database (asynchronous).

        :param  project_id: The ID of the project to which the feedback data belongs.
        :param message: The content of the feedback.
        :param source: The source of the feedback.
        :param user_id: Optional ID of the user who provided the feedback.
        :param chat_id: Optional ID of the chat associated with the feedback.
        :param date: Optional date the feedback was given.
        :return: Response from the API.
        """
        url = f"{self.__base_url}/data/{project_id}/feedback/add"
        payload = {
            "message": message,
            "source": source,
        }
        if user_id is not None:
            payload["user_id"] = user_id
        if chat_id is not None:
            payload["chat_id"] = chat_id
        if date:
            payload["date"] = date

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=self.__headers)
            response.raise_for_status()
            return response.json()
