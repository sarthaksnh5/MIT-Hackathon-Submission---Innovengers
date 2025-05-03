import {View} from 'react-native';
import React from 'react';
import {useAuthStore} from '../../store/useAuthStore';
import ButtonComponent from '../../components/ButtonComponent/ButtonComponent';

const SettingScreen = ({navigation}) => {
  const {logout} = useAuthStore();

  const handleLogout = () => {
    logout();
    navigation.reset({
      index: 0,
      routes: [{name: 'Login'}],
    });
  };

  return (
    <View className="w-full h-full flex p-2">
      <View className="w-full">
        <ButtonComponent onPress={handleLogout} className="w-full bg-red-500">
          Logout
        </ButtonComponent>
      </View>
    </View>
  );
};

export default SettingScreen;
