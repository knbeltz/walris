import { useSignIn } from '@clerk/expo';
import { useSignInWithGoogle } from '@clerk/expo/google';
import { useSignInWithApple } from '@clerk/expo/apple';
import { useState } from 'react';
import { TextInput, View } from 'react-native';
import { useRouter } from 'expo-router';

import { Button } from '@/components/ui/button';
import { Text } from '@/components/ui/text';

export default function SignInScreen() {
    const { signIn, errors, fetchStatus } = useSignIn();

    const { startGoogleAuthenticationFlow } = useSignInWithGoogle();
    const { startAppleAuthenticationFlow } = useSignInWithApple();

    const router = useRouter();

    // Phone authentication state 
    const [phoneNumber, setPhoneNumber] = useState('');
    const[verificationCode, setVerificationCode] = useState('');
    const [isVerifying, setIsVerifying] = useState(false);

    // General UI state 
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    // Authentication handlers will go here 
    const handlePhoneSignIn = async () => {
        const normalizedPhoneNumber = phoneNumber.trim();

        if (!normalizedPhoneNumber) {
            setErrorMessage('Please enter your phone number.')
            return;
        }

        setIsSubmitting(true);
        setErrorMessage('');


        try {
            // Create a sign-in attempt using the phone number. 
            const { error } = await signIn.create({
                identifier: normalizedPhoneNumber,
            });
            if (error) {
                setErrorMessage(
                    error.message ?? 'Unable to begin phone sign-in',
                );
                return;
            }

            // Send the SMS verification code. 
            const result = await signIn.phoneCode.sendCode({
                phoneNumber: normalizedPhoneNumber,
            });
            
            if (result.error) {
                setErrorMessage(
                    result.error.message ?? 'Unable to send verification code.',
                );
                return;
            }

            setIsVerifying(true);
        } catch (error: unknown) {
            console.error('Phone sign-in error:', error);
            setErrorMessage(error instanceof Error ? error.message : 'Something went wrong.');
        }   finally {
            setIsSubmitting(false);
        }
    };

    const handleVerifyingPhoneCode = async () => {
        const normalizedCode = verificationCode.trim()

        if (!normalizedCode) {
            setErrorMessage('Please enter the verifcation code.');
            return;
        }

        setIsSubmitting(true);
        setErrorMessage('')

        try {
            const { error } = await signIn.phoneCode.verifyCode({
                code: normalizedCode,
            });

            if (error) {
                setErrorMessage (
                    error.message ?? 'The verification code is invalid.'
                );
                return;
            }

            if (signIn.status !== 'complete') {
                setErrorMessage(
                    'Sign-in requires another authentication step.'
                );
                return;
            }

            await signIn.finalize({
                navigate: ({ session }) => {
                    if (session?.currentTask) {
                        console.log(
                            'Clerk session task still required',
                            session.currentTask,
                        );
                    }
                }
            })
        }
    }



    return(
        <View>
            <Text>Sign In</Text>

            <TextInput   
                value={phoneNumber}
                onChangeText={setPhoneNumber}
                placeholder="+1 202 555 0123"
                keyboardType="phone-pad"
            />

            {isVerifying && (
                <TextInput
                    value={verificationCode}
                    onChangeText={setVerificationCode}
                    placeholder="Verification code"
                    keyboardType="number-pad"
                
                />
            )}

            {errorMessage ? <Text>{errorMessage}</Text> : null}

            <Button disabled={isSubmitting}>
                <Text>Continue with phone</Text>
            </Button>

            <Button disabled={isSubmitting}>
                <Text>Continue with Google</Text>
            </Button>

            <Button disabled={isSubmitting}>
                <Text>Continue with Apple</Text>
            </Button>
        </View>
    );
}