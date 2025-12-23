from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from users.forms import SignupForm, LoginForm
from utils.email import send_email

User = get_user_model()


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        signer = TimestampSigner()
        signed_email = signer.sign(user.email)
        code = signing.dumps(signed_email)

        verify_url = self.request.build_absolute_uri(
            f"/users/verify/?code={code}"
        )

        send_email(
            subject="[Todo] 이메일 인증",
            message=f"아래 링크를 클릭해 인증을 완료하세요.\n\n{verify_url}",
            to_email=user.email,
        )

        return render(self.request, "registration/signup_done.html")


def verify_email(request):
    code = request.GET.get("code")

    signer = TimestampSigner()
    try:
        signed_email = signing.loads(code)
        email = signer.unsign(signed_email, max_age=60 * 5)
    except (SignatureExpired, BadSignature, TypeError):
        return render(request, "registration/verify_failed.html")

    user = get_object_or_404(User, email=email)
    user.is_active = True
    user.save()

    return render(request, "registration/verify_success.html")


class LoginView(FormView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("cbv_todo_list")

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
