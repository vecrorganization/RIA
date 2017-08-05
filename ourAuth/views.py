# Django
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from braces.views import LoginRequiredMixin
# App
from ourAuth.forms import SignUpForm
from ourAuth.tokens import account_activation_token
from ourAuth.models import AddressUser


@login_required
def home(request):
    '''
    Template view showed to user when email is confirmed
    '''
    return render(request, 'ourAuth/home.html')

class SignUp(TemplateView):
    template_name = 'ourAuth/signup/signup.html'

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        context['form'] = SignUpForm()
        return context

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your RIA Account'
            message = render_to_string('ourAuth/signup/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')

        return render(request, self.template_name, {'form': form})


class ManageAddress(LoginRequiredMixin,TemplateView):
    """
    Manage address
    """
    template_name = 'ourAuth/address/manage_address.html'

    def get_context_data(self, **kwargs):
        context = super(ManageAddress, self).get_context_data(**kwargs)
        context['addresses'] = AddressUser.objects.filter(user = self.request.user)
        context['Title'] = "Manejar direcciones"
        return context


def account_activation_sent(request):
    return render(request, 'ourAuth/signup/account_activation_sent.html')


def activate(request, uidb64, token):
    """
    Activate account when email is confirmed
    """

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('homeAuth')
    else:
        return render(request, 'ourAuth/signup/account_activation_invalid.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu contraseña se actualizó correctamente.')
            return redirect('Products')
        else:
            messages.error(request, 'Corrija por favor el error abajo.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password/change_password.html', {
        'form': form
    })