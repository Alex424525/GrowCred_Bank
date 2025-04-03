from django.contrib import admin
<<<<<<< HEAD
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'bank_name', 'user', 'balance', 'is_active', 'created_at')
    list_filter = ('bank_name', 'is_active')
    search_fields = ('account_number', 'user__username')
    readonly_fields = ('account_number', 'created_at', 'updated_at')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'transaction_type', 'description', 'created_at')
    search_fields = ('account__account_number', 'description')
    list_filter = ('transaction_type', 'created_at')
=======
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.html import format_html
from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'bank_name', 'user', 'balance', 'is_active', 'created_at', 'delete_button')
    list_filter = ('bank_name', 'is_active')
    search_fields = ('account_number', 'user__username', 'user__email', 'user__phone_number')
    readonly_fields = ('account_number', 'created_at', 'updated_at')

    fieldsets = (
        ('계좌 정보', {
            'fields': ('user', 'account_number', 'bank_name', 'account_name', 'balance', 'password')
        }),
        ('상태 정보', {
            'fields': ('is_active',)
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # 삭제 버튼 추가
    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color: #ba2121; color: white; padding: 3px 10px;" '
            'href="{}">삭제</a>',
            reverse('admin:delete_account', args=[obj.pk])
        )

    delete_button.short_description = '계좌 삭제'

    # 커스텀 URL 추가
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:account_id>/delete/',
                self.admin_site.admin_view(self.delete_account_view),
                name='delete_account',
            ),
        ]
        return custom_urls + urls

    # 삭제 기능 구현
    def delete_account_view(self, request, account_id):
        account = self.get_object(request, account_id)

        # 잔액이 0인지 확인
        if account.balance > 0:
            self.message_user(
                request,
                f"계좌 '{account.account_number}'의 잔액이 0이 아니므로 삭제할 수 없습니다. 잔액: {account.balance}",
                level=messages.ERROR
            )
        else:
            # 계좌번호 저장
            account_number = account.account_number

            # 계좌 삭제
            account.delete()

            self.message_user(
                request,
                f"계좌 '{account_number}'가 성공적으로 삭제되었습니다.",
                level=messages.SUCCESS
            )

        # 리다이렉트
        return HttpResponseRedirect(reverse('admin:accounts_account_changelist'))

    # 계좌 생성 시 계좌번호 자동 생성
    def save_model(self, request, obj, form, change):
        if not change:  # 신규 계좌 생성 시
            obj.account_number = Account.generate_account_number()
        super().save_model(request, obj, form, change)


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    fields = ('transaction_type', 'amount', 'description', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    can_delete = False
    max_num = 10  # 최대 10개까지만 표시


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'transaction_type', 'description', 'created_at', 'delete_button')
    search_fields = ('account__account_number', 'description', 'account__user__username', 'account__user__email')
    list_filter = ('transaction_type', 'created_at', 'account__bank_name')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('거래 정보', {
            'fields': ('account', 'transaction_type', 'amount', 'description')
        }),
        ('시스템 정보', {
            'fields': ('created_at',)
        }),
    )

    # 삭제 버튼 추가
    def delete_button(self, obj):
        return format_html(
            '<a class="button" style="background-color: #ba2121; color: white; padding: 3px 10px;" '
            'href="{}">삭제</a>',
            reverse('admin:delete_transaction', args=[obj.pk])
        )

    delete_button.short_description = '거래 삭제'

    # 커스텀 URL 추가
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:transaction_id>/delete/',
                self.admin_site.admin_view(self.delete_transaction_view),
                name='delete_transaction',
            ),
        ]
        return custom_urls + urls

    # 삭제 기능 구현
    def delete_transaction_view(self, request, transaction_id):
        transaction = self.get_object(request, transaction_id)
        account = transaction.account

        # 트랜잭션 정보 저장
        transaction_info = f"{transaction.get_transaction_type_display()} {transaction.amount}"

        # 트랜잭션 삭제 시 잔액 조정
        if transaction.transaction_type == 'DEPOSIT':
            # 입금 취소 시 잔액 감소
            if account.balance >= transaction.amount:
                account.balance -= transaction.amount
                account.save()

                # 트랜잭션 삭제
                transaction.delete()

                self.message_user(
                    request,
                    f"거래 '{transaction_info}'가 삭제되었습니다. 계좌 잔액이 조정되었습니다.",
                    level=messages.SUCCESS
                )
            else:
                self.message_user(
                    request,
                    f"계좌 잔액이 부족하여 입금 취소를 할 수 없습니다.",
                    level=messages.ERROR
                )

        elif transaction.transaction_type == 'WITHDRAW' or transaction.transaction_type == 'TRANSFER':
            # 출금/이체 취소 시 잔액 증가
            account.balance += transaction.amount
            account.save()

            # 트랜잭션 삭제
            transaction.delete()

            self.message_user(
                request,
                f"거래 '{transaction_info}'가 삭제되었습니다. 계좌 잔액이 조정되었습니다.",
                level=messages.SUCCESS
            )

        # 리다이렉트
        return HttpResponseRedirect(reverse('admin:accounts_transaction_changelist'))


# Admin 사이트 커스터마이징
admin.site.site_header = '은행 관리 시스템'
admin.site.site_title = '은행 관리'
admin.site.index_title = '관리자 페이지'
>>>>>>> main
