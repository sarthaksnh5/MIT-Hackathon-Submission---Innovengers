import {Image, View} from 'react-native';
import React, {useState} from 'react';
import CardComponent from '../../components/CardComponent/CardComponent';
// @ts-ignore
import logo from '../../assets/img/logo.png';
import TextComponent from '../../components/TextComponent/TextComponent';
import ButtonComponent from '../../components/ButtonComponent/ButtonComponent';
import InputComponent from '../../components/InputComponent/InputComponent';
import DividerComponent from '../../components/DividerComponent/DividerComponent';
import {useApi} from '../../hooks/useApi';
import {registerURL} from '../../constants/urls';
import {showGlobalSnackbar} from '../../hooks/useSnackbar';
import {useNavigation} from '@react-navigation/native';

const RegisterScreen = () => {
  const [userData, setUserData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const [showPassword, setShowPassword] = useState(false);
  const navigation = useNavigation();

  const api = useApi();

  const handleSubmit = async () => {
    if (!userData.email || !userData.password) {
      showGlobalSnackbar('Please fill in all the fields', 'red');
      return;
    }

    try {
      const response = await api.request(
        registerURL,
        'POST',
        {
          username: userData.username,
          email: userData.email,
          password: userData.password,
          password_confirm: userData.confirmPassword,
        },
        {
          requireAuth: false,
          successMessage: 'Register successful',
        },
      );

      console.log('response', response);

      // Assuming response is returned from api.request
      if (response?.data) {
        navigation.goBack();
      } else {
        showGlobalSnackbar('Registration failed. Please try again.', 'red');
      }
    } catch (error) {
      console.error(error);
      showGlobalSnackbar('Something went wrong. Please try again.', 'red');
    }
  };

  return (
    <View className="w-full h-full flex items-center justify-center bg-theme p-2">
      <CardComponent>
        <Image source={logo} style={{width: 60, height: 60}} />

        <TextComponent variant={'bodyLarge'} style={{fontWeight: 'bold'}}>
          Register Yourself!!!
        </TextComponent>

        <View className="w-full p-2">
          <InputComponent
            label="Username"
            placeholder="Enter your username"
            inputClassName="text-base"
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                username: e,
              });
            }}
            left={{
              icon: 'account',
            }}
          />
        </View>

        <View className="w-full p-2">
          <InputComponent
            label="Email"
            placeholder="Enter your email"
            inputClassName="text-base"
            keyboardType="email-address"
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                email: e,
              });
            }}
            left={{
              icon: 'account',
            }}
          />
        </View>

        <View className="w-full p-2">
          <InputComponent
            label="Password"
            placeholder="Enter your password"
            inputClassName="text-base"
            secureTextEntry={!showPassword}
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                password: e,
              });
            }}
            left={{
              icon: 'lock',
            }}
            right={{
              icon: showPassword ? 'eye-off' : 'eye',
              onPress: () => {
                // Handle icon press
                setShowPassword(!showPassword);
              },
            }}
          />
        </View>

        <View className="w-full p-2">
          <InputComponent
            label="Confirm Password"
            placeholder="Enter your confirm password"
            inputClassName="text-base"
            secureTextEntry={!showPassword}
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                confirmPassword: e,
              });
            }}
            left={{
              icon: 'lock',
            }}
            right={{
              icon: showPassword ? 'eye-off' : 'eye',
              onPress: () => {
                // Handle icon press
                setShowPassword(!showPassword);
              },
            }}
          />
        </View>

        <View className="w-full p-2">
          <ButtonComponent
            onPress={handleSubmit}
            loading={api.loading}
            disabled={api.loading}>
            Sign Up
          </ButtonComponent>
        </View>

        <View className="w-full p-2">
          <DividerComponent />
        </View>

        <View className="w-full p-2">
          <ButtonComponent
            mode={'outlined'}
            onPress={() => {
              navigation.goBack();
            }}>
            Login
          </ButtonComponent>
        </View>
      </CardComponent>
      <TextComponent variant={'bodyLarge'} style={{color: '#fff'}}>
        Personal AI CRM
      </TextComponent>
    </View>
  );
};

export default RegisterScreen;
