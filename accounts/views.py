from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions
from .models import Account, Transaction
from .forms import AccountForm
from .serializers import AccountSerializer


# REST API ViewSet
class AccountViewSet(viewsets.ModelViewSet):
    """계좌 API ViewSet"""
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """로그인한 사용자의 계좌만 반환"""
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """계좌 생성 시 자동으로 사용자와 계좌번호 설정"""
        account_number = Account.generate_account_number()
        serializer.save(user=self.request.user, account_number=account_number)

# 웹 뷰 함수
@login_required
def personal_banking(request):
    """개인 뱅킹 메인 페이지 - 계좌 목록 표시"""
    accounts = Account.objects.filter(user=request.user, is_active=True)
    return render(request, 'users/account_inquiry.html', {'accounts': accounts})


@login_required
def create_account(request):
    """계좌 개설 페이지"""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.account_number = Account.generate_account_number()
            account.save()
            messages.success(request, '계좌가 성공적으로 개설되었습니다!')
            return redirect('accounts:personal_banking')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user, is_active=True)

    return render(request, 'personal_banking/create_account.html', {
        'form': form,
        'accounts': accounts,
    })


@login_required
def account_detail(request, account_id):
    """계좌 상세 정보 페이지"""
    # 상세 페이지가 없으므로 계좌 조회 페이지로 리디렉션
    return redirect('users:accounts_inquiry')


@login_required
def delete_account(request, account_id):
    """계좌 삭제 기능"""
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == 'POST':
        password = request.POST.get('password')

        # 비밀번호 확인
        if password != account.password:
            messages.error(request, '계좌 비밀번호가 일치하지 않습니다.')
            return redirect('users:accounts_inquiry')

        # 잔액이 있는 계좌는 삭제 불가
        if account.balance > 0:
            messages.error(request, '잔액이 있는 계좌는 삭제할 수 없습니다. 먼저 잔액을 출금해주세요.')
            return redirect('users:accounts_inquiry')

        # 계좌 비활성화 (실제 삭제 대신)
        account.is_active = False
        account.save()

        messages.success(request, '계좌가 성공적으로 삭제되었습니다.')
        return redirect('users:accounts_inquiry')

    return redirect('users:accounts_inquiry')


@login_required
def delete_selected_accounts(request):
    """선택한 계좌 일괄 삭제"""
    if request.method == 'POST':
        password = request.POST.get('password')
        selected_account_ids = request.POST.get('selected_account_ids', '').split(',')

        if not selected_account_ids or selected_account_ids[0] == '':
            messages.error(request, '삭제할 계좌를 선택해주세요.')
            return redirect('users:accounts_inquiry')

        deletion_errors = []
        deletion_success = 0

        for account_id in selected_account_ids:
            try:
                account = Account.objects.get(id=account_id, user=request.user)

                # 비밀번호 확인
                if password != account.password:
                    deletion_errors.append(f"{account.account_name}: 비밀번호가 일치하지 않습니다.")
                    continue

                # 잔액이 있는 계좌는 삭제 불가
                if account.balance > 0:
                    deletion_errors.append(f"{account.account_name}: 잔액이 있는 계좌는 삭제할 수 없습니다.")
                    continue

                # 계좌 비활성화 (실제 삭제 대신)
                account.is_active = False
                account.save()
                deletion_success += 1

            except Account.DoesNotExist:
                deletion_errors.append(f"ID {account_id}: 계좌를 찾을 수 없습니다.")

        if deletion_success > 0:
            messages.success(request, f'{deletion_success}개의 계좌가 성공적으로 삭제되었습니다.')

        if deletion_errors:
            for error in deletion_errors:
                messages.error(request, error)

        return redirect('users:accounts_inquiry')

    return redirect('users:accounts_inquiry')