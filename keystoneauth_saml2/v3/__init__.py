# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from keystoneauth_saml2.v3 import adfs
from keystoneauth_saml2.v3 import saml2

ADFSToken = adfs.ADFSToken
Saml2Token = saml2.Saml2Token

__all__ = ['ADFSToken',
           'Saml2Token']
