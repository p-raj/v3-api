from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    This adapter attaches the user signing in or
    signing up to the `Organization` if it exists.
    """
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        You can use this hook to intervene, e.g. abort the login by
        raising an ImmediateHttpResponse

        Why both an adapter hook and the signal? Intervening in
        e.g. the flow from within a signal handler is bad -- multiple
        handlers may be active and are executed in undetermined order.
        """
        # TODO
        pass

    def new_user(self, request, sociallogin):
        """
        Instantiates a new User instance.
        """
        # TODO
        return super(SocialAccountAdapter, self).new_user(request, sociallogin)
