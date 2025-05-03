import {View, Text, Image, TouchableOpacity} from 'react-native';
import React from 'react';

import Entypo from 'react-native-vector-icons/Entypo';
import AntDesign from 'react-native-vector-icons/AntDesign';

const StoryCover = () => {
  return (
    <View
      className="w-2/5 bg-white rounded-lg mb-3 flex flex-col gap-2"
      style={{elevation: 1}}>
      <Image
        className="w-full h-48 rounded-lg"
        source={{
          uri: 'https://placeit-img-1-p.cdn.aws.placeit.net/uploads/stage/stage_image/22739/optimized_large_thumb_children-stories-book-cover-541__1_.jpg',
        }}
        resizeMode={'stretch'}
      />
      <View className="absolute top-0 right-0 p-2 bg-white bg-opacity-80 rounded-lg">
        <Text className="text-sm">10 min read</Text>
      </View>

      <View className="flex bg-opacity-80 ml-2">
        <Text className="text-lg font-bold">Story Title</Text>
        <Text className="text-sm">Author Name</Text>
      </View>
      {/* icon Button rows to edit, published, delete */}
      <View className="flex flex-row items-center justify-around mb-3">
        <TouchableOpacity>
          <Entypo name="edit" size={20} color="black" />
        </TouchableOpacity>
        <TouchableOpacity>
          <AntDesign name="checkcircle" size={20} color="green" />
        </TouchableOpacity>
        <TouchableOpacity>
          <AntDesign name="delete" size={20} color="red" />
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default StoryCover;
