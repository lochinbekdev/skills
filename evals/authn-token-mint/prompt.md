---
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
---

Review the authentication of this service with the audit-authn skill. There is no running
environment and there are no test accounts, so this is a static-only engagement: do not
interview me, reply with the report as your final message.

`routes/api.php`
```php
Route::post('/auth/login', [AuthController::class, 'login'])->middleware('throttle:5,1');

Route::middleware('client.basic')->group(function () {
    Route::post('/client/sso/token', [ClientSsoController::class, 'token']);
});
```

`app/Http/Controllers/AuthController.php`
```php
class AuthController extends Controller
{
    public function login(LoginRequest $request)
    {
        $user = User::where('email', $request->email)->first();
        if (! $user || ! Hash::check($request->password, $user->password)) {
            return response()->json(['message' => 'Invalid credentials'], 401);
        }
        return ['token' => auth('api')->login($user)];
    }
}
```

`app/Http/Controllers/ClientSsoController.php`
```php
class ClientSsoController extends Controller
{
    // Partner systems call this to obtain a session for one of our users.
    public function token(Request $request)
    {
        $request->validate(['national_id' => 'required|string|size:14']);
        $user = User::where('national_id', $request->national_id)->firstOrFail();
        return ['token' => auth('api')->login($user)];
    }
}
```

`app/Http/Middleware/ClientBasicAuth.php`
```php
class ClientBasicAuth
{
    public function handle($request, Closure $next)
    {
        $client = Client::where('username', $request->getUser())->first();
        if (! $client || ! Hash::check($request->getPassword(), $client->secret)) {
            abort(401);
        }
        return $next($request);
    }
}
```
