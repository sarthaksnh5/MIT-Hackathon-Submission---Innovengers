import {View, Image} from 'react-native';
import React, {useEffect} from 'react';
// @ts-ignore
import logo from '../../assets/img/logo.png';
import {ActivityIndicator} from 'react-native-paper';
import TextComponent from '../../components/TextComponent/TextComponent';
import {useAuthStore} from '../../store/useAuthStore';
import {useNavigation} from '@react-navigation/native';
import CardComponent from '../../components/CardComponent/CardComponent';

const SplashScreen = () => {
  const {isLoggedIn} = useAuthStore();
  const navigation = useNavigation();

  useEffect(() => {
    setTimeout(() => {
      if (isLoggedIn) {
        navigation.reset({
          index: 0,
          // @ts-ignore
          routes: [{name: 'BottomStack'}],
        });
      } else {
        navigation.reset({
          index: 0,
          // @ts-ignore
          routes: [{name: 'Login'}],
        });
      }
    }, 3000);
  }, [isLoggedIn, navigation]);

  return (
    <View className="w-full h-full flex items-center justify-center bg-theme gap-2">
      <CardComponent>
        <Image source={logo} style={{width: 100, height: 100}} />
        <ActivityIndicator size={'large'} />
      </CardComponent>
      <TextComponent variant={'bodyLarge'} style={{color: '#fff'}}>
        Personal AI CRM
      </TextComponent>
    </View>
  );
};

export default SplashScreen;
