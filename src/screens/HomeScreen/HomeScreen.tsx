import {FlatList, View} from 'react-native';
import React, {useEffect, useState} from 'react';
import {Text} from 'react-native-paper';
import {useApi} from '../../hooks/useApi';
import {contactURL} from '../../constants/urls';
import TextComponent from '../../components/TextComponent/TextComponent';

const HomeScreen = () => {
  const contactApi = useApi();
  const [contacts, setContacts] = useState({
    count: 0,
    data: [],
  });

  const getContacts = async () => {
    try {
      const response = await contactApi.request(contactURL, 'GET', null, {
        requireAuth: true,
        showSnackbar: false,
      });

      if (response.error) {
        console.log('Error fetching contacts:', Response.error);
      }

      if (response.data) {
        setContacts({
          count: response.data.count,
          data: response.data.results,
        });
      }
    } catch (e) {
      console.log('Error fetching contacts:', e);
    }
  };

  useEffect(() => {
    getContacts();

    return () => {};
  }, []);

  return (
    // <View className="w-full h-full flex items-center">
    <View className="w-full h-full flex p-4">
      <View className="w-full flex flex-row items-center justify-around gap-2 mb-2">
        {/* Card */}
        <View className="w-2/5 h-32 bg-purple-400 rounded-lg flex items-center justify-center p-3">
          <Text
            variant={'bodyLarge'}
            style={{color: '#fff', fontWeight: 'bold'}}>
            Contact
          </Text>
          <Text style={{color: '#fff', fontWeight: 'bold'}}>
            {contacts.count}
          </Text>
        </View>

        <View className="w-2/5 h-32 bg-blue-400 rounded-lg flex items-center justify-center p-3">
          <Text
            style={{color: '#fff', fontWeight: 'bold', textAlign: 'center'}}>
            Connection Request
          </Text>
          <Text style={{color: '#fff', fontWeight: 'bold'}}>40</Text>
        </View>
      </View>

      <TextComponent>Contacts</TextComponent>
      <FlatList
        data={contacts.data}
        keyExtractor={(item, index) => item.id.toString()}
        renderItem={({item}) => (
          <View className="w-full h-16 bg-gray-200 rounded-lg flex p-3 mb-2">
            <Text>
              {item.first_name} {item.last_name}
            </Text>
            
          </View>
        )}
        showsVerticalScrollIndicator={false}
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={{paddingBottom: 100}}
      />
    </View>
  );
};

export default HomeScreen;
