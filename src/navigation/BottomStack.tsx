// BottomStack.tsx
import React from 'react';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';
import Entypo from 'react-native-vector-icons/Entypo';
import ProfileScreen from '../screens/ProfileScreen/ProfileScreen';
import SettingScreen from '../screens/SettingScreen/SettingScreen';
import TextComponent from '../components/TextComponent/TextComponent';
import {Image, TouchableOpacity} from 'react-native';
// @ts-ignore
import logo from '../assets/img/logo.png';
import MaterialIcons from 'react-native-vector-icons/MaterialIcons';
import ChatScreen from '../screens/ChatScreen/ChatScreen';
import HomeScreen from '../screens/HomeScreen/HomeScreen';
import PlusScreen from '../screens/PlusScreen/PlusScreen';

const Tab = createBottomTabNavigator();

const homeTabBarIcon = ({color, size}: {color: string; size: number}) => (
  <Entypo name="home" size={size} color={color} />
);

const ChatTabBarIcon = ({color, size}: {color: string; size: number}) => (
  <Entypo name="chat" size={size} color={color} />
);

const PlusTabBarIcon = ({color, size}: {color: string; size: number}) => (
  <Entypo name="circle-with-plus" size={size} color={color} />
);

const profileTabBarIcon = ({color, size}: {color: string; size: number}) => (
  <Ionicons name="person" size={size} color={color} />
);

const settingsTabBarIcon = ({color, size}: {color: string; size: number}) => (
  <Ionicons name="settings" size={size} color={color} />
);

const CustomHeader = ({navigation}: any) => {
  return {
    headerTitle: () => (
      <TextComponent style={{fontSize: 18, fontWeight: 'bold'}}>
        {'Personal CRM'}
      </TextComponent>
    ),
    headerLeft: () => (
      <Image
        source={logo} // Replace with your logo path
        style={{width: 30, height: 30, marginLeft: 15}}
        resizeMode="contain"
      />
    ),
    headerRight: () => (
      <TouchableOpacity onPress={() => console.log('Menu opened')}>
        <MaterialIcons name="more-vert" size={24} style={{marginRight: 15}} />
      </TouchableOpacity>
    ),
  };
};

const BottomStack = () => {
  return (
    <Tab.Navigator
      initialRouteName="Home"
      screenOptions={({navigation}) => ({
        tabBarActiveTintColor: 'tomato',
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: {backgroundColor: 'white'},
        headerShown: true,
        ...CustomHeader({navigation}),
      })}>
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarIcon: homeTabBarIcon,
        }}
      />
      <Tab.Screen
        name="Chat"
        component={ChatScreen}
        options={{
          tabBarIcon: ChatTabBarIcon,
        }}
      />
      <Tab.Screen
        name="Plus"
        component={PlusScreen}
        options={{
          tabBarIcon: PlusTabBarIcon,
          tabBarLabel: 'Add',
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          tabBarIcon: profileTabBarIcon,
        }}
      />
      <Tab.Screen
        name="Settings"
        component={SettingScreen}
        options={{
          tabBarIcon: settingsTabBarIcon,
        }}
      />
    </Tab.Navigator>
  );
};

export default BottomStack;
