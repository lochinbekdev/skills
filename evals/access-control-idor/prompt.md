---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

Review the authorization of this small API with the audit-access-control skill. There is no
running environment and there are no test accounts, so this is a static-only engagement: do
not interview me, reply with the report as your final message.

`routes/api.php`
```php
Route::middleware('auth:api')->group(function () {
    Route::get('/invoices', [InvoiceController::class, 'index']);
    Route::get('/invoices/{id}', [InvoiceController::class, 'show']);
    Route::delete('/invoices/{id}', [InvoiceController::class, 'destroy']);
});
```

`app/Http/Controllers/InvoiceController.php`
```php
class InvoiceController extends Controller
{
    public function index(Request $request)
    {
        return Invoice::where('user_id', $request->user()->id)->paginate(20);
    }

    public function show(Request $request, int $id)
    {
        return Invoice::findOrFail($id);
    }

    public function destroy(Request $request, int $id)
    {
        $invoice = Invoice::findOrFail($id);
        $this->authorize('delete', $invoice);
        $invoice->delete();
        return response()->noContent();
    }
}
```

`app/Policies/InvoicePolicy.php`
```php
class InvoicePolicy
{
    public function delete(User $user, Invoice $invoice): bool
    {
        return $user->id === $invoice->user_id;
    }
}
```
