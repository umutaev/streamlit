# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional

from redis import Redis

from streamlit.runtime.session_manager import SessionInfo, SessionStorage


class KeyDBSessionStorage(SessionStorage):
    def __init__(
        self,
        redis_instance: Redis,
        redis_key_prefix: str,
        maxsize: int = 128,
        ttl_seconds: int = 2 * 60,  # 2 minutes
    ):
        self._redis = redis_instance
        self._redis_key_prefix = redis_key_prefix
        self._maxsize = maxsize
        self._cache_ttl = ttl_seconds

    def get(self, session_id: str) -> Optional[SessionInfo]:
        if not self._redis.exists(self._redis_key_prefix + session_id):
            # As it returns 0 if nothing was found.
            return None
        self._redis.get(self._redis_key_prefix + session_id)
        # TODO: assembling session_info

    def save(self, session_info: SessionInfo) -> None:
        # TODO: saving session_info
        pass

    def delete(self, session_id: str) -> None:
        self._redis.delete(self._redis_key_prefix + session_id)

    def list(self) -> List[SessionInfo]:
        list(self._redis.scan_iter(self._redis_key_prefix + "*"))
        # TODO: assembling session_infos
