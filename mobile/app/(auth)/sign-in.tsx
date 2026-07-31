import { useSignIn, useSSO, useAuth  } from '@clerk/expo';
import { useState, useEffect } from 'react';
import { TextInput, View } from 'react-native';
import { useRouter } from 'expo-router';
import * as AuthSession from 'expo-auth-session';

import { Button } from '@/components/ui/button';
import { Text } from '@/components/ui/text';
import { redirectAfterAuth } from '@/lib/redirectAfterAuth'
import { getErrorMessage } from '@/lib/utils';

export default function SignInScreen() {
  const { isSignedIn, getToken } = useAuth();

  const { signIn, errors, fetchStatus } = useSignIn();

  const { startSSOFlow } = useSSO();

  const router = useRouter();

  useEffect(() => {
    if (isSignedIn) {
      void redirectAfterAuth(getToken, router);
    }
  }, [isSignedIn, getToken, router]);

  const redirectUrl = AuthSession.makeRedirectUri({
    path: 'sso-callback',
  });

  // Email authentication state
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  // General UI state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleEmailPasswordSignIn = async () => {
    // ...validation on email/password...
    const normalizedEmail = email.trim();

    if (!normalizedEmail) {
      setErrorMessage('Please enter your email address.');
      return;
    }
    
    if (!password) {
      setErrorMessage('Please enter your password.');
      return;
    }

    setIsSubmitting(true);
    setErrorMessage('');

    try {
      const { error } = await signIn.password({
        emailAddress: normalizedEmail, password
      });

      if (error) {
        setErrorMessage(error.message ?? 'Unable to sign-in.');
        return;
      }

      if (signIn.status !== 'complete') {
        setErrorMessage('Sign-in requires another authentication step.');
        return;
      }

      await signIn.finalize({
        navigate: async ({ session }) => {
          if (session?.currentTask) {
            console.log(
              'Clerk session task still required',
              session.currentTask,
            );
            return;
          }

          await redirectAfterAuth(getToken, router)
        },
      });
    } catch (error: unknown) {
      console.error('Email/password sign-in error:', error);
      setErrorMessage(getErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setIsSubmitting(true);
    setErrorMessage('');

    try {
      const { createdSessionId, setActive } = await startSSOFlow({
        strategy: 'oauth_google',
        redirectUrl,
      });

      if (!createdSessionId) {
        setErrorMessage(
          'Google authentication requires an additional step.',
        );
        return;
      }

      if (!setActive) {
        setErrorMessage('Unable to activate the Google session.');
        return;
      }

      await setActive({
        session: createdSessionId,
        navigate: async ({ session }) => {
          if (session?.currentTask) {
            console.log(
              'Clerk session task still required:',
              session.currentTask,
            );
            return;
          }

          await redirectAfterAuth(getToken, router);
        },
      });
    } catch (error: unknown) {
      console.error('Google SSO error:', error);
      setErrorMessage(getErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleAppleSignIn = async () => {
    setIsSubmitting(true);
    setErrorMessage('');

    try {
      const { createdSessionId, setActive } = await startSSOFlow({
        strategy: 'oauth_apple',
        redirectUrl,
      });

      if (!createdSessionId || !setActive) {
        setErrorMessage('Apple sign-in could not be completed.');
        return;
      }

      await setActive({
        session: createdSessionId,
      });

      await redirectAfterAuth(getToken, router);
    } catch (error: unknown) {
      console.error('Apple SSO error:', error);
      setErrorMessage(getErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  const clerkIsFetching = fetchStatus === 'fetching';
  const authenticationIsLoading = isSubmitting || clerkIsFetching;

  return (
    <View style={{ flex: 1, padding: 24, justifyContent: 'center', gap: 16 }}>
      <Text>Sign In</Text>

      <TextInput
        value={email}
        onChangeText={setEmail}
        placeholder="you@example.com"
        keyboardType="email-address"
        autoComplete="email"
        autoCapitalize="none"
        editable={!authenticationIsLoading}
      />
      {errors.fields.identifier ? (
        <Text>{errors.fields.identifier.message}</Text>
      ) : null}

      <TextInput
        value={password}
        onChangeText={setPassword}
        placeholder="Password"
        secureTextEntry
        autoComplete="password"
        autoCapitalize="none"
        editable={!authenticationIsLoading}
      />
      {errors.fields.password ? (
        <Text>{errors.fields.password.message}</Text>
      ) : null}

      <Button onPress={handleEmailPasswordSignIn} disabled={authenticationIsLoading}>
        <Text>{authenticationIsLoading ? 'Signing in...' : 'Sign in'}</Text>
      </Button>

      <Button onPress={handleGoogleSignIn} disabled={authenticationIsLoading}>
        <Text>Continue with Google</Text>
      </Button>

      <Button onPress={handleAppleSignIn} disabled={authenticationIsLoading}>
        <Text>Continue with Apple</Text>
      </Button>

      {errorMessage ? <Text>{errorMessage}</Text> : null}
    </View>
  );
}
