import {Image, ScrollView, TouchableOpacity, View} from 'react-native';
import React, {useState} from 'react';

import {launchImageLibrary} from 'react-native-image-picker';
import Entypo from 'react-native-vector-icons/Entypo';
import InputComponent from '../../components/InputComponent/InputComponent';
import {ActivityIndicator, Text} from 'react-native-paper';
import {useApi} from '../../hooks/useApi';
import {contactURL, linkedURL, ocrURL} from '../../constants/urls';
import TextComponent from '../../components/TextComponent/TextComponent';
import {showGlobalSnackbar} from '../../hooks/useSnackbar';
import ButtonComponent from '../../components/ButtonComponent/ButtonComponent';

const PlusScreen = ({navigation}) => {
  const [photo, setPhoto] = useState<any>(null);

  const {request, loading} = useApi();
  const linkedUseApi = useApi();

  const [linkedExtractedData, setLinkedExtractedData] = useState(null);

  const [userData, setUserData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    company: '',
    job_title: '',
    linkedin_url: '',
    linkedin_username: '',
    notes: '',
  });

  const handlePickImage = () => {
    launchImageLibrary(
      {
        mediaType: 'photo',
        includeBase64: false,
      },
      response => {
        if (response.didCancel) {
          console.log('User cancelled image picker');
        } else if (response.errorCode) {
          console.error('ImagePicker Error:', response.errorMessage);
        } else if (response.assets && response.assets.length > 0) {
          console.log('ImagePicker Response:', response);
          setPhoto(response.assets[0]);
        }
      },
    );
  };

  const extractTextFromImage = async (imageUri: string) => {
    // we need to make request with image to extract text
    const formData = new FormData();
    formData.append('file', {
      uri: imageUri,
      name: 'image.jpg',
      type: 'image/jpeg',
    });
    formData.append('language', 'eng');

    try {
      // Step 1: Upload the image to the OCR processing system
      const uploadFormData = new FormData();
      uploadFormData.append('image', {
        uri: imageUri,
        name: 'business_card.jpg',
        type: 'image/jpeg',
      });
      uploadFormData.append('image_type', 'BUSINESS_CARD');
      // Optionally add location and taken_date if available
      // uploadFormData.append('location', 'Conference, New York');
      // uploadFormData.append('taken_date', '2025-05-02T08:00:00Z');

      const uploadResponse = await request(ocrURL, 'POST', uploadFormData, {
        requireAuth: true,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (uploadResponse.error) {
        console.log('Error uploading image:', uploadResponse.error);
        return;
      }

      const processResponse = await request(
        `${ocrURL}${uploadResponse.data.id}/process/`,
        'POST',
        null,
        {
          requireAuth: true,
        },
      );

      if (processResponse.error) {
        console.log('Error processing image:', processResponse.error);
        return;
      }

      console.log('Processed Data:', processResponse.data.processed_text);

      try {
        let processedData = processResponse.data.processed_text;
        // If processed_text is a string, try to parse it as JSON
        if (typeof processedData === 'string') {
          processedData = JSON.parse(processedData);
        }
        setUserData({
          ...userData,
          first_name: processedData.first_name || '',
          last_name: processedData.last_name || '',
          email: processedData.email || '',
          phone_number: processedData.phone_number || '',
          company: processedData.company || '',
          job_title: processedData.job_title || '',
          linkedin_username: processedData.linkedin_username || '',
          notes: processedData.notes || '',
        });
      } catch (e) {
        console.log('Error parsing processed data:', e);
        showGlobalSnackbar('Unabel to parse data', 'red');
      }

      // if (processResponse && processResponse.raw_text) {
      //   // Do something with the extracted text, e.g., update state
      //   console.log('Extracted Text:', processResponse.raw_text);
      //   // Optionally, parse and set userData fields here
      // } else {
      //   throw new Error('Failed to process image with OCR');
      // }
    } catch (error) {
      console.log('OCR extraction error:', error);
    }
  };

  const handleBusinessExtraction = () => {
    launchImageLibrary(
      {
        mediaType: 'photo',
        includeBase64: false,
      },
      response => {
        if (response.didCancel) {
          console.log('User cancelled image picker');
        } else if (response.errorCode) {
          console.error('ImagePicker Error:', response.errorMessage);
        } else if (response.assets && response.assets.length > 0) {
          // @ts-ignore
          extractTextFromImage(response.assets[0].uri);
        }
      },
    );
  };

  const extractLinkedInProfile = async () => {
    try {
      const response = await linkedUseApi.request(
        `${linkedURL}fetch_linkedin/`,
        'POST',
        {
          username: userData.linkedin_username,
        },
        {
          requireAuth: true,
          successMessage: 'LinkedIn profile extracted successfully',
        },
      );

      if (response.error) {
        console.log('Error extracting LinkedIn profile:', response.error);
        showGlobalSnackbar('Unable to extract LinkedIn profile', 'red');
        return;
      }

      // Assuming the response contains the extracted data
      console.log(response.data);
      setLinkedExtractedData(response.data);
    } catch (e) {
      console.log('Error extracting LinkedIn profile:', e);
    }
  };

  const submitContact = async () => {
    try {
      const response = await request(
        contactURL,
        'POST',
        {
          first_name: userData.first_name,
          last_name: userData.last_name,
          email: userData.email,
          phone_number: userData.phone_number,
          company: userData.company,
          job_title: userData.job_title,
          linkedin_url: userData.linkedin_url,
          notes: userData.notes,
        },
        {
          requireAuth: true,
          successMessage: 'Contact submitted successfully',
        },
      );

      if (response.error) {
        console.log('Error submitting contact:', response.error);
        showGlobalSnackbar('Unable to submit contact', 'red');
        return;
      }

      if (linkedExtractedData != null) {
        const fetchResponse = await request(
          `${linkedURL}fetch_linkedin_data/`,
          'POST',
          {
            contact_id: response.data.id,
            username: userData.linkedin_username,
          },
          {
            requireAuth: true,
            showSnackbar: false,
          },
        );
      }

      setUserData({
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
        company: '',
        job_title: '',
        linkedin_url: '',
        linkedin_username: '',
        notes: '',
      });
      setPhoto(null);

      navigation.goBack();
    } catch (e) {
      console.log('Error submitting contact:', e);
    }
    // Handle the response from the server
  };

  return (
    <ScrollView contentContainerClassName="p-2 gap-2">
      <View className="w-full h-32 flex items-center justify-center">
        <TouchableOpacity
          className="w-32 h-32 bg-gray-200 rounded-full items-center justify-center"
          onPress={handlePickImage}>
          {photo ? (
            <Image
              source={{uri: photo.uri}}
              // eslint-disable-next-line react-native/no-inline-styles
              style={{width: '100%', height: '100%', borderRadius: 50}}
            />
          ) : (
            <Entypo name="edit" size={50} color="#000" />
          )}
        </TouchableOpacity>
      </View>

      <View className="w-full p-2 flex items-center justify-center">
        {loading ? (
          <View>
            <Text>Extracting Information...</Text>
            <ActivityIndicator />
          </View>
        ) : (
          <TouchableOpacity onPress={handleBusinessExtraction}>
            <Text>Extract Information Through Business Card</Text>
          </TouchableOpacity>
        )}
      </View>

      <View className="w-full flex flex-row items-center justify-center gap-2">
        <View className="w-1/2">
          <InputComponent
            label="First Name"
            placeholder="Enter your first name"
            inputClassName="text-base"
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                first_name: e,
              });
            }}
            left={{
              icon: 'account',
            }}
            value={userData.first_name}
          />
        </View>

        <View className="w-1/2">
          <InputComponent
            label="Last Name"
            placeholder="Enter your last name"
            inputClassName="text-base"
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                last_name: e,
              });
            }}
            left={{
              icon: 'account',
            }}
            value={userData.last_name}
          />
        </View>
      </View>

      <View className="w-full flex flex-row items-center justify-center gap-2 mb-2">
        <View className="w-1/2">
          <InputComponent
            label="Email"
            placeholder="Enter your email"
            inputClassName="text-base"
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                email: e,
              });
            }}
            left={{
              icon: 'email',
            }}
            value={userData.email}
          />
        </View>

        <View className="w-1/2">
          <InputComponent
            label="Phone Number"
            placeholder="Enter your phone number"
            inputClassName="text-base"
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                phone_number: e,
              });
            }}
            left={{
              icon: 'phone',
            }}
            value={userData.phone_number}
          />
        </View>
      </View>

      <TextComponent variant={'headlineSmall'} className="text-center my-2">
        Professional Infromation
      </TextComponent>

      <View className="w-full flex flex-row items-center justify-center gap-2">
        <View className="w-1/2">
          <InputComponent
            label="Company"
            placeholder="Enter your company name"
            inputClassName="text-base"
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                company: e,
              });
            }}
            left={{
              icon: 'office-building',
            }}
          />
        </View>

        <View className="w-1/2">
          <InputComponent
            label="Job Title"
            placeholder="Enter your job title"
            inputClassName="text-base"
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                job_title: e,
              });
            }}
            left={{
              icon: 'briefcase',
            }}
          />
        </View>
      </View>

      <View className="w-full flex flex-row items-center justify-center gap-2 mb-2">
        <View className="w-2/3">
          <InputComponent
            label="LinkedIn Username"
            placeholder="Enter your LinkedIn username"
            inputClassName="text-base"
            autoCapitalize="none"
            onChangeText={e => {
              setUserData({
                ...userData,
                linkedin_username: e,
              });
            }}
            left={{
              icon: 'linkedin',
            }}
            value={userData.linkedin_username}
          />
        </View>

        <View className="w-1/3 flex items-center justify-center">
          {linkedUseApi.loading ? (
            <ActivityIndicator />
          ) : (
            <TouchableOpacity onPress={extractLinkedInProfile}>
              <Text
                style={{
                  color: '#0077B5',
                  textDecorationLine: 'underline',
                }}>
                Verify Profile
              </Text>
            </TouchableOpacity>
          )}
        </View>
      </View>

      {linkedExtractedData != null && (
        <View className="w-full">
          <View className="w-full flex flex-row items-center justify-center gap-2">
            <View className="w-1/5 flex items-center justify-center">
              <Image
                // @ts-ignore
                source={{uri: linkedExtractedData.profilePicture}}
                style={{width: 75, height: 75, borderRadius: 50}}
              />
            </View>
            <View className="w-4/5 flex flex-col items-center justify-center">
              <TextComponent variant={'headlineSmall'}>
                {linkedExtractedData.firstName} {linkedExtractedData.lastName}
              </TextComponent>
              <TextComponent variant={'bodyMedium'}>
                {linkedExtractedData.headline}
              </TextComponent>
              <TextComponent variant={'bodyMedium'}>
                {linkedExtractedData.location}
              </TextComponent>
              <TextComponent variant={'bodyMedium'}>
                {linkedExtractedData.company}
              </TextComponent>
            </View>
          </View>
        </View>
      )}

      <View className="w-full mb-3">
        <ButtonComponent onPress={submitContact}>Submit</ButtonComponent>
      </View>

      <View className="w-full">
        <ButtonComponent
          mode={'elevated'}
          onPress={() => {
            setUserData({
              first_name: '',
              last_name: '',
              email: '',
              phone_number: '',
              company: '',
              job_title: '',
              linkedin_url: '',
              linkedin_username: '',
              notes: '',
            });
            setPhoto(null);
          }}>
          Reset
        </ButtonComponent>
      </View>
    </ScrollView>
  );
};

export default PlusScreen;
