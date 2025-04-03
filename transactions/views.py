from itertools import chain
from operator import attrgetter

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from accounts.models import Account
from transactions.forms import DepositForm, WithdrawalForm
from transactions.models import DepositModel, WithdrawalModel


# 입금 기능
class DepositCreateView(LoginRequiredMixin, CreateView):
    model = DepositModel    # 입금 모델
    form_class = DepositForm    # 입금 폼
    template_name = 'transactions/transactions_deposit_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')  # URL에서 받은 pk 값을 템플릿에 전달
        return context

    # POST 요청이 들어오면 폼을 검증하고 데이터 저장
    # request : 요청 객체
    # *args, **kwargs: 추가적인 URL 매개변수를 받을 수 있도록 함
    def form_valid(self, form):
        # 저장하기 전에 객체 생성만 함
        deposit = form.save(commit=False)
        # 현재 요청된 사용자의 계좌 정보 가져오기

        account_pk = self.request.POST.get('account')

        # if not account_pk:
        #     return Http404

        try:
            account = get_object_or_404(Account, pk=account_pk, user=self.request.user)
        except:
            messages.error(self.request, "잘못된 계좌입니다.")
            return self.form_invalid(form)

        # 본인 계좌가 맞는지 확인
        if deposit.account != account or deposit.account is None:
            # messages : "from django.contrib import messages"
            # 에러 메시지를 출력
            messages.error(self.request, "잘못된 계좌입니다. 본인의 계좌만 사용해 주세요.")
            # 폼이 유효하지 않다고 처리하고 다시 입금 폼 렌더링
            return self.form_invalid(form)
        # 계좌 설정 후 저장
        # balance는 Decimal필드라 save()가 없음
        deposit.account = account # deposit과 account(사용자 계좌) 연결 유지
        # account.balance(입금 완료된 현재 잔액) = account.balance(현재 잔액을 가져옴) + deposit.amount(폼 객체에 입금 금액 입력해서 더함)
        account.balance += deposit.amount # account.balance = account.balance + deposit.amount : 더하고 재할당
        # 사용자 계좌 저장(DB에 저장)
        account.save()
        # 실제 입금 금액 저장
        deposit.save()

        # 확인 메시지를 출력
        messages.success(self.request, "입금이 정상적으로 처리 되었습니다.")
        # 입금 페이지로 이동
        return HttpResponseRedirect(self.get_success_url()) # 아래 def get_success_url()에서 받아옴

    # 입금페이지로 이동
    def get_success_url(self):
        return reverse_lazy('transactions:deposit') # 입금페이지로 이동


# 출금 기능
class WithdrawalCreateView(LoginRequiredMixin, CreateView):
    model = WithdrawalModel # 출금 모델
    template_name = 'transactions/transactions_withdrawal_form.html'
    form_class = WithdrawalForm
    success_url = reverse_lazy('transactions:withdrawal')  # 출금 성공 후 이동할 페이지

    # def get_object(self, queryset=None):
    #     """
    #     현재 로그인한 사용자의 출금 내역만 조회할 수 있도록 제한.
    #     존재하지 않는 pk라면 404 에러 처리.
    #     """
    #     account = get_object_or_404(Account, user=self.request.user)
    #     withdrawal = get_object_or_404(WithdrawalModel, pk=self.kwargs['pk'], account=account)
    #
    #     return withdrawal

    # 출금 로직
    def form_valid(self, form):
        # DB에 저장 하기전 객체만 생성
        withdrawal = form.save(commit=False)
        # 현재 요청된 사용자의 계좌 정보 가져오기
        # account = get_object_or_404(Account, user=self.request.user)
        accounts = Account.objects.filter(user=self.request.user)
        # 사용자의 계좌가 없을 경우
        if not accounts:
            messages.error(self.request, "계좌가 없습니다.")
            return self.form_invalid(form)

        # 폼에서 선택한 계좌 사용
        account_pk = self.request.POST.get('account')
        account = get_object_or_404(Account, pk=account_pk, user=self.request.user)


        # 출금 가능 여부 확인
        if account.balance >= withdrawal.amount: # 사용자 계좌의 잔액이 출금 금액보다 크거나 같으면
            account.balance -= withdrawal.amount # 사용자 계좌에서 잔액을 차감한다.
            account.save()  # 차감한 잔액 저장
            withdrawal.save() # 출금 정보 저장
            messages.success(self.request, "출금이 정상적으로 처리 되었습니다.") # 성공 메시지 출력
            return super().form_valid(form)
        else:
            messages.error(self.request, "잔액이 부족합니다.") # 잔액 부족시 실패 메시지 출력
            return self.form_invalid(form)


# 현재 로그인 되어있는 사용자 게좌의 여태까지 한 입금,출금들의 내역을 볼수 있게 한다.
class TransactionListView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transactions_list.html'
    context_object_name = 'transactions'
    paginate_by = 10    # 페이지당 표시할 거래수

    def get_queryset(self):
        # 로그인한 사용자의 모든 계좌 가져오기
        user_accounts = Account.objects.filter(user=self.request.user)

        # 사용자에게 계좌가 없는 경우 빈 리스트 반환
        if not user_accounts:
            return []

        # 해당 계좌들의 모든 입급 내역 가져오기
        deposits = DepositModel.objects.filter(account__in=user_accounts).select_related('account')

        # 해당 계좌들의 모든 출금 내역 가져오기
        withdrawals = WithdrawalModel.objects.filter(account__in=user_accounts).select_related('account')

        # 입급과 출금 내역을 합치고 날짜 기준으로 정렬
        # 각 객체에 거래 타입 표시를 위한 속성 추가
        for deposit in deposits:
            deposit.transaction_type = '입금'
            deposit.transaction_date = deposit.deposit_at # 입금 날짜 필드가 있다 가정

        for withdrawal in withdrawals:
            withdrawal.transaction_type = '출금'
            withdrawal.transaction_date = withdrawal.withdrawal_at # 출금 날짜 필드가 있다 가정

        # 입금과 출금 내역을 합치고 날짜 기준으로 내림차순 정렬(최신 거래가 위에 오도록)
        all_transactions = sorted(
            chain(deposits, withdrawals),
            key=attrgetter('transaction_date'),
            reverse=True
        )

        return all_transactions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 사용자의 모든 계좌 정보 전달
        user_accounts = Account.objects.filter(user=self.request.user)
        context['accounts'] = user_accounts

        # 계좌가 없는 경우 확인 메시지 추가
        if not user_accounts.exists():
            context['no_accounts'] = True  # 계좌 없음 표시

        return context






