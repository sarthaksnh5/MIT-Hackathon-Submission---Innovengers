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
import {loginURL} from '../../constants/urls';
import {showGlobalSnackbar} from '../../hooks/useSnackbar';
import {useAuthStore} from '../../store/useAuthStore';
import {useNavigation} from '@react-navigation/native';

const LoginScreen = () => {
  const [userData, setUserData] = useState({
    email: '',
    password: '',
  });

  const [showPassword, setShowPassword] = useState(false);
  const navigation = useNavigation();

  const api = useApi();
  const {login} = useAuthStore();

  const handleSubmit = async () => {
    if (!userData.email || !userData.password) {
      showGlobalSnackbar('Please fill in all the fields', 'red');
      return;
    }

    try {
      const response = await api.request(
        loginURL,
        'POST',
        {
          username: userData.email,
          password: userData.password,
        },
        {
          requireAuth: false,
          successMessage: 'Login successful',
        },
      );

      // Assuming response is returned from api.request
      if (response?.data) {
        login({
          refresh_token: response.data.refresh,
          access_token: response.data.access,
        });

        navigation.reset({
          index: 0,
          // @ts-ignore
          routes: [{name: 'BottomStack'}],
        });
      } else {
        showGlobalSnackbar('Login failed. Please try again.', 'red');
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
          Welcome Back!!!
        </TextComponent>

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
          <ButtonComponent
            onPress={handleSubmit}
            loading={api.loading}
            disabled={api.loading}>
            Login
          </ButtonComponent>
        </View>

        <View className="w-full p-2">
          <DividerComponent />
        </View>

        <View className="w-full p-2">
          <ButtonComponent
            mode={'outlined'}
            onPress={() => {
              navigation.navigate('Register');
            }}>
            Sign Up
          </ButtonComponent>
        </View>
      </CardComponent>
      <TextComponent variant={'bodyLarge'} style={{color: '#fff'}}>
        Personal AI CRM
      </TextComponent>
    </View>
  );
};

export default LoginScreen;
