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

import abc

from keystoneclient.auth.identity import v3
from oslo.config import cfg
import six


@six.add_metaclass(abc.ABCMeta)
class FederatedAuthPlugin(v3.AuthConstructor):

    def __init__(self, auth_url,
                 identity_provider,
                 identity_provider_url,
                 **kwargs):
        """Class constructor accepting following parameters:

        :param auth_url: URL of the Identity Service
        :type auth_url: string
        :param identity_provider: name of the Identity Provider the client
                                  will authenticate against. This parameter
                                  will be used to build a dynamic URL used to
                                  obtain unscoped OpenStack token.
        :type identity_provider: string

        :param identity_provider_url: An Identity Provider URL, where the SAML2
                                      authn request will be sent.
        :type identity_provider_url: string

        """
        super(FederatedAuthPlugin, self).__init__(auth_url=auth_url, **kwargs)
        self.identity_provider = identity_provider
        self.identity_provider_url = identity_provider_url

    @abc.abstractproperty
    def protocol(self):
        """Return name of the protocol name used for federated workflow."""

    @abc.abstractproperty
    def scoped_token_plugin(self):
        """Return class that should be used for scoping the token."""

    @classmethod
    def get_options(cls):
        options = super(FederatedAuthPlugin, cls).get_options()
        options.extend([
            cfg.StrOpt('identity-provider', help="Identity Provider's name"),
            cfg.StrOpt('identity-provider-url',
                       help="Identity Provider's URL"),
        ])
        return options

    @property
    def token_url(self):
        """Return full URL where authorization data is sent."""
        values = {
            'host': self.auth_url.rstrip('/'),
            'identity_provider': self.identity_provider,
            'protocol': self.protocol
        }
        url = ("%(host)s/OS-FEDERATION/identity_providers/"
               "%(identity_provider)s/protocols/%(protocol)s/auth")
        url = url % values

        return url

    @property
    def _scoping_data(self):
        return {'trust_id': self.trust_id,
                'domain_id': self.domain_id,
                'domain_name': self.domain_name,
                'project_id': self.project_id,
                'project_name': self.project_name,
                'project_domain_id': self.project_domain_id,
                'project_domain_name': self.project_domain_name}

    def get_auth_ref(self, session, **kwargs):
        """Authenticate via SAML2 protocol and retrieve unscoped token.

        This is a multi-step process where a client does federated authn
        receives an unscoped token.

        Federated authentication utilizing SAML2 Enhanced Client or Proxy
        extension. See ``Saml2Token_get_unscoped_auth_ref()``
        for more information on that step.
        Upon successful authentication and assertion mapping an
        unscoped token is returned and stored within the plugin object for
        further use.

        :param session :a session object to send out HTTP requests.
        :type session: keystoneclient.session.Session

        :return access.AccessInfoV3: an object with scoped token's id and
                                     unscoped token json included.

        """
        auth_ref = self.get_unscoped_auth_ref(session)

        if any(self._scoping_data.values()):
            token_plugin = self.scoped_token_plugin(self.auth_url,
                                                    token=auth_ref.auth_token,
                                                    **self._scoping_data)

            auth_ref = token_plugin.get_auth_ref(session)

        return auth_ref

    @abc.abstractmethod
    def get_unscoped_auth_ref(self, session, **kwargs):
        """Fetch unscoped federated token."""
