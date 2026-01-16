import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  TextInput,
  ScrollView,
  ActivityIndicator,
  Alert,
  Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as ImagePicker from 'expo-image-picker';
import { COLORS, SIZES, FONTS, SHADOWS } from '../theme';
import { db, storage } from '../firebase.config';
import { collection, addDoc, serverTimestamp } from 'firebase/firestore';
import { ref, uploadBytes, getDownloadURL } from 'firebase/storage';

const UploadMealPlanScreen = ({ navigation }) => {
  const [image, setImage] = useState(null);
  const [week, setWeek] = useState('');
  const [year, setYear] = useState('');
  const [notes, setNotes] = useState('');
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    requestPermissions();
    setCurrentWeekAndYear();
  }, []);

  const requestPermissions = async () => {
    if (Platform.OS !== 'web') {
      const cameraPermission = await ImagePicker.requestCameraPermissionsAsync();
      const mediaPermission = await ImagePicker.requestMediaLibraryPermissionsAsync();

      if (cameraPermission.status !== 'granted' || mediaPermission.status !== 'granted') {
        Alert.alert(
          'Berechtigung erforderlich',
          'Bitte erlauben Sie den Zugriff auf Kamera und Fotobibliothek.'
        );
      }
    }
  };

  const setCurrentWeekAndYear = () => {
    const now = new Date();
    const weekNum = getWeekNumber(now);
    setWeek(weekNum.week.toString());
    setYear(weekNum.year.toString());
  };

  const getWeekNumber = (date) => {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);
    d.setDate(d.getDate() + 3 - ((d.getDay() + 6) % 7));
    const week1 = new Date(d.getFullYear(), 0, 4);
    const weekNum = 1 + Math.round(((d - week1) / 86400000 - 3 + ((week1.getDay() + 6) % 7)) / 7);
    return { week: weekNum, year: d.getFullYear() };
  };

  const pickImageFromCamera = async () => {
    try {
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [3, 4],
        quality: 0.8,
      });

      if (!result.canceled && result.assets[0]) {
        setImage(result.assets[0].uri);
      }
    } catch (error) {
      Alert.alert('Fehler', 'Kamera konnte nicht geöffnet werden.');
      console.error('Kamera-Fehler:', error);
    }
  };

  const pickImageFromGallery = async () => {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [3, 4],
        quality: 0.8,
      });

      if (!result.canceled && result.assets[0]) {
        setImage(result.assets[0].uri);
      }
    } catch (error) {
      Alert.alert('Fehler', 'Galerie konnte nicht geöffnet werden.');
      console.error('Galerie-Fehler:', error);
    }
  };

  const uploadImage = async () => {
    if (!image) {
      Alert.alert('Fehler', 'Bitte wählen Sie zuerst ein Bild aus.');
      return;
    }

    if (!week || !year) {
      Alert.alert('Fehler', 'Bitte geben Sie Woche und Jahr ein.');
      return;
    }

    const weekNum = parseInt(week);
    const yearNum = parseInt(year);

    if (isNaN(weekNum) || weekNum < 1 || weekNum > 53) {
      Alert.alert('Fehler', 'Bitte geben Sie eine gültige Wochennummer ein (1-53).');
      return;
    }

    if (isNaN(yearNum) || yearNum < 2020 || yearNum > 2030) {
      Alert.alert('Fehler', 'Bitte geben Sie ein gültiges Jahr ein.');
      return;
    }

    try {
      setUploading(true);

      // Bild zu Storage hochladen
      const response = await fetch(image);
      const blob = await response.blob();
      const filename = `mealplans/${yearNum}/week_${weekNum}_${Date.now()}.jpg`;
      const storageRef = ref(storage, filename);

      await uploadBytes(storageRef, blob);
      const downloadURL = await getDownloadURL(storageRef);

      // Daten in Firestore speichern
      await addDoc(collection(db, 'mealPlans'), {
        week: weekNum,
        year: yearNum,
        imageUrl: downloadURL,
        notes: notes.trim(),
        createdAt: serverTimestamp(),
      });

      Alert.alert(
        'Erfolg',
        'Speiseplan erfolgreich hochgeladen!',
        [
          {
            text: 'OK',
            onPress: () => {
              setImage(null);
              setNotes('');
              setCurrentWeekAndYear();
              navigation.goBack();
            },
          },
        ]
      );
    } catch (error) {
      console.error('Upload-Fehler:', error);
      Alert.alert('Fehler', 'Upload fehlgeschlagen. Bitte versuchen Sie es erneut.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[COLORS.primaryDark, COLORS.background]}
        style={styles.gradient}
      >
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <Text style={styles.backButtonText}>←</Text>
          </TouchableOpacity>
          <View style={styles.headerContent}>
            <Text style={styles.headerTitle}>UPLOAD</Text>
            <Text style={styles.headerSubtitle}>Speiseplan hinzufügen</Text>
          </View>
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {/* Bildauswahl */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>BILD AUSWÄHLEN</Text>

            {image ? (
              <View style={[styles.imagePreviewContainer, SHADOWS.medium]}>
                <Image source={{ uri: image }} style={styles.imagePreview} />
                <TouchableOpacity
                  style={styles.removeImageButton}
                  onPress={() => setImage(null)}
                >
                  <Text style={styles.removeImageButtonText}>✕</Text>
                </TouchableOpacity>
              </View>
            ) : (
              <View style={styles.imagePlaceholder}>
                <Text style={styles.placeholderIcon}>📸</Text>
                <Text style={styles.placeholderText}>Kein Bild ausgewählt</Text>
              </View>
            )}

            <View style={styles.buttonRow}>
              <TouchableOpacity
                style={[styles.halfButton, styles.primaryButton]}
                onPress={pickImageFromCamera}
                disabled={uploading}
              >
                <Text style={styles.halfButtonIcon}>📷</Text>
                <Text style={styles.buttonText}>Kamera</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.halfButton, styles.secondaryButton]}
                onPress={pickImageFromGallery}
                disabled={uploading}
              >
                <Text style={styles.halfButtonIcon}>🖼️</Text>
                <Text style={styles.buttonText}>Galerie</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Wochendaten */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>KALENDERWOCHE</Text>

            <View style={styles.inputRow}>
              <View style={styles.halfInputContainer}>
                <Text style={styles.inputLabel}>Woche</Text>
                <TextInput
                  style={styles.input}
                  placeholder="1-53"
                  placeholderTextColor={COLORS.textDisabled}
                  value={week}
                  onChangeText={setWeek}
                  keyboardType="number-pad"
                  maxLength={2}
                  editable={!uploading}
                />
              </View>

              <View style={styles.halfInputContainer}>
                <Text style={styles.inputLabel}>Jahr</Text>
                <TextInput
                  style={styles.input}
                  placeholder="2024"
                  placeholderTextColor={COLORS.textDisabled}
                  value={year}
                  onChangeText={setYear}
                  keyboardType="number-pad"
                  maxLength={4}
                  editable={!uploading}
                />
              </View>
            </View>
          </View>

          {/* Notizen */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>HINWEISE (OPTIONAL)</Text>
            <TextInput
              style={[styles.input, styles.textArea]}
              placeholder="z.B. Besondere Menüs, Allergiehinweise..."
              placeholderTextColor={COLORS.textDisabled}
              value={notes}
              onChangeText={setNotes}
              multiline
              numberOfLines={4}
              textAlignVertical="top"
              editable={!uploading}
            />
          </View>

          {/* Upload Button */}
          <TouchableOpacity
            style={[
              styles.uploadButton,
              SHADOWS.medium,
              uploading && styles.buttonDisabled,
            ]}
            onPress={uploadImage}
            disabled={uploading}
          >
            {uploading ? (
              <>
                <ActivityIndicator color={COLORS.text} size="small" />
                <Text style={[styles.uploadButtonText, { marginLeft: 12 }]}>
                  WIRD HOCHGELADEN...
                </Text>
              </>
            ) : (
              <Text style={styles.uploadButtonText}>HOCHLADEN</Text>
            )}
          </TouchableOpacity>

          <View style={styles.bottomSpacer} />
        </ScrollView>
      </LinearGradient>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  gradient: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingTop: 50,
    paddingHorizontal: SIZES.padding,
    paddingBottom: SIZES.paddingLarge,
    borderBottomWidth: 2,
    borderBottomColor: COLORS.accent,
  },
  backButton: {
    width: 44,
    height: 44,
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radius,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SIZES.padding,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  backButtonText: {
    fontSize: 24,
    color: COLORS.accent,
    fontWeight: 'bold',
  },
  headerContent: {
    flex: 1,
  },
  headerTitle: {
    ...FONTS.h2,
    color: COLORS.accent,
    fontWeight: '800',
    letterSpacing: 2,
  },
  headerSubtitle: {
    ...FONTS.caption,
    color: COLORS.textSecondary,
    marginTop: 4,
    letterSpacing: 1,
  },
  content: {
    flex: 1,
  },
  section: {
    padding: SIZES.paddingLarge,
  },
  sectionTitle: {
    ...FONTS.bodyBold,
    color: COLORS.accent,
    letterSpacing: 2,
    marginBottom: SIZES.padding,
  },
  imagePreviewContainer: {
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radiusLarge,
    overflow: 'hidden',
    borderWidth: 2,
    borderColor: COLORS.border,
    marginBottom: SIZES.padding,
  },
  imagePreview: {
    width: '100%',
    height: 300,
    resizeMode: 'contain',
    backgroundColor: COLORS.surfaceLight,
  },
  removeImageButton: {
    position: 'absolute',
    top: 12,
    right: 12,
    width: 36,
    height: 36,
    backgroundColor: COLORS.danger,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
  },
  removeImageButtonText: {
    color: COLORS.white,
    fontSize: 20,
    fontWeight: 'bold',
  },
  imagePlaceholder: {
    height: 200,
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radiusLarge,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: COLORS.border,
    borderStyle: 'dashed',
    marginBottom: SIZES.padding,
  },
  placeholderIcon: {
    fontSize: 48,
    marginBottom: SIZES.paddingSmall,
  },
  placeholderText: {
    ...FONTS.body,
    color: COLORS.textSecondary,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: SIZES.padding,
  },
  halfButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: SIZES.padding,
    borderRadius: SIZES.radiusLarge,
    borderWidth: 2,
  },
  primaryButton: {
    backgroundColor: COLORS.primary,
    borderColor: COLORS.accent,
  },
  secondaryButton: {
    backgroundColor: COLORS.secondary,
    borderColor: COLORS.border,
  },
  halfButtonIcon: {
    fontSize: 20,
    marginRight: 8,
  },
  buttonText: {
    ...FONTS.bodyBold,
    color: COLORS.text,
  },
  inputRow: {
    flexDirection: 'row',
    gap: SIZES.padding,
  },
  halfInputContainer: {
    flex: 1,
  },
  inputLabel: {
    ...FONTS.bodyBold,
    color: COLORS.text,
    marginBottom: SIZES.paddingSmall,
  },
  input: {
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radius,
    padding: SIZES.padding,
    ...FONTS.body,
    color: COLORS.text,
    borderWidth: 2,
    borderColor: COLORS.border,
  },
  textArea: {
    minHeight: 100,
    textAlignVertical: 'top',
  },
  uploadButton: {
    backgroundColor: COLORS.success,
    borderRadius: SIZES.radiusLarge,
    padding: SIZES.paddingLarge,
    marginHorizontal: SIZES.paddingLarge,
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'row',
    borderWidth: 3,
    borderColor: COLORS.accent,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  uploadButtonText: {
    ...FONTS.h4,
    color: COLORS.text,
    fontWeight: '800',
    letterSpacing: 2,
  },
  bottomSpacer: {
    height: 40,
  },
});

export default UploadMealPlanScreen;
