import { useSignUp, useSSO, useAuth } from '@clerk/expo';
import { useState, useEffect, useRef } from 'react';
import { TextInput, View } from 'react-native';
import { useRouter } from 'expo-router';
import * as AuthSession from 'expo-auth-session';

import { Button } from '@/components/ui/button';
import { Text } from '@/components/ui/text';
import { redirectAfterAuth } from '@/lib/redirectAfterAuth';
import { getErrorMessage } from '@/lib/utils';

export default function SignUpScreen() {
  const { isSignedIn, getToken } = useAuth();

  const { signUp, errors, fetchStatus } = useSignUp();

  const { startSSOFlow } = useSSO();

  const router = useRouter();

  const hasRedirected = useRef(false);

  useEffect(() => {
    if (isSignedIn && !hasRedirected.current) {
      void redirectAfterAuth(getToken, router);
    }
  }, [isSignedIn, getToken, router]);

  const redirectUrl = AuthSession.makeRedirectUri({
    path: 'sso-callback',
  });

  // Email authentication state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [verificationCode, setVerificationCode] = useState('');
  const [isVerifying, setIsVerifying] = useState(false);

  // General ui state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleEmailPasswordSignUp = async () => {
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
      const { error } = await signUp.password({
        emailAddress: normalizedEmail,
        password,
      });

      if (error) {
        setErrorMessage(error.message ?? 'Unable to sign up.');
        return;
      }

      const result = await signUp.verifications.sendEmailCode();

      if (result.error) {
        setErrorMessage(
          result.error.message ?? 'Unable to send verification code.',
        );
        return;
      }

      setIsVerifying(true);
    } catch (error: unknown) {
      console.error('Email/password sign-up error:', error);
      setErrorMessage(getErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleVerifyingEmailCode = async () => {
    const normalizedCode = verificationCode.trim();

    if (!normalizedCode) {
      setErrorMessage('Please enter the verification code.');
      return;
    }

    setIsSubmitting(true);
    setErrorMessage('');

    try {
      const { error } = await signUp.verifications.verifyEmailCode({
        code: normalizedCode,
      });

      if (error) {
        setErrorMessage(error.message ?? 'The verification code is invalid.');
        return;
      }

      if (signUp.status !== 'complete') {
        setErrorMessage('Sign-up requires another authentication step.');
        return;
      }

      hasRedirected.current = true;

      await signUp.finalize({
        navigate: async ({ session }) => {
          if (session?.currentTask) {
            console.log(
              'Clerk session task still required',
              session.currentTask,
            );
            return;
          }

          if (!session) {
            throw new Error('No Clerk session after sign-up.');
          }

          await redirectAfterAuth(
            () => session.getToken(), 
            router,
          );
        },
      });
    } catch (error: unknown) {
      console.error('Email verification error:', error);
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
        setErrorMessage('Google authentication requires an additional step.');
        return;
      }

      if (!setActive) {
        setErrorMessage('Unable to activate the Google session.');
        return;
      }

      hasRedirected.current = true;

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

          if (!session) {
            throw new Error('No Clerk session after Google sign-in.');
          }

          await redirectAfterAuth(
            () => session.getToken(), 
            router,
          );
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

      hasRedirected.current = true;

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

          if (!session) {
            throw new Error('No Clerk session after Apple sign-in.')
          }

          await redirectAfterAuth(
            () => session.getToken(),
            router,
          );
        }
      });

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
      <Text>Sign Up</Text>

      {!isVerifying ? (
        <>
          <TextInput
            value={email}
            onChangeText={setEmail}
            placeholder="you@example.com"
            keyboardType="email-address"
            autoComplete="email"
            autoCapitalize="none"
            editable={!authenticationIsLoading}
          />
          {errors.fields.emailAddress ? (
            <Text>{errors.fields.emailAddress.message}</Text>
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

          <Button
            onPress={handleEmailPasswordSignUp}
            disabled={authenticationIsLoading}
          >
            <Text>
              {authenticationIsLoading
                ? 'Sending code...'
                : 'Continue with email'}
            </Text>
          </Button>

          <Button
            onPress={handleGoogleSignIn}
            disabled={authenticationIsLoading}
          >
            <Text>Continue with Google</Text>
          </Button>

          <Button
            onPress={handleAppleSignIn}
            disabled={authenticationIsLoading}
          >
            <Text>Continue with Apple</Text>
          </Button>
        </>
      ) : (
        <>
          <TextInput
            value={verificationCode}
            onChangeText={setVerificationCode}
            placeholder="Verification code"
            keyboardType="number-pad"
            autoComplete="one-time-code"
            editable={!authenticationIsLoading}
          />
          {errors.fields.code ? (
            <Text>{errors.fields.code.message}</Text>
          ) : null}

          <Button
            onPress={handleVerifyingEmailCode}
            disabled={authenticationIsLoading}
          >
            <Text>
              {authenticationIsLoading ? 'Verifying...' : 'Verify code'}
            </Text>
          </Button>
        </>
      )}

      {errorMessage ? <Text>{errorMessage}</Text> : null}
    </View>
  );
}
