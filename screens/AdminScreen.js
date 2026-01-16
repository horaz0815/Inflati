import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, SIZES, FONTS, SHADOWS } from '../theme';
import { auth } from '../firebase.config';
import { signInWithEmailAndPassword, signOut, onAuthStateChanged } from 'firebase/auth';

const AdminScreen = ({ navigation }) => {
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setInitialLoading(false);
    });

    return unsubscribe;
  }, []);

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Fehler', 'Bitte geben Sie E-Mail und Passwort ein.');
      return;
    }

    try {
      setLoading(true);
      await signInWithEmailAndPassword(auth, email, password);
      Alert.alert('Erfolg', 'Erfolgreich angemeldet!');
      setEmail('');
      setPassword('');
    } catch (error) {
      let errorMessage = 'Anmeldung fehlgeschlagen.';
      if (error.code === 'auth/user-not-found') {
        errorMessage = 'Benutzer nicht gefunden.';
      } else if (error.code === 'auth/wrong-password') {
        errorMessage = 'Falsches Passwort.';
      } else if (error.code === 'auth/invalid-email') {
        errorMessage = 'Ungültige E-Mail-Adresse.';
      }
      Alert.alert('Fehler', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      Alert.alert('Erfolg', 'Erfolgreich abgemeldet!');
    } catch (error) {
      Alert.alert('Fehler', 'Abmeldung fehlgeschlagen.');
    }
  };

  if (initialLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.accent} />
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
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
            <Text style={styles.headerTitle}>ADMIN</Text>
            <Text style={styles.headerSubtitle}>Verwaltungsbereich</Text>
          </View>
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {!user ? (
            // Login Form
            <View style={styles.loginContainer}>
              <View style={[styles.card, SHADOWS.medium]}>
                <Text style={styles.cardTitle}>AUTHENTIFIZIERUNG</Text>
                <Text style={styles.cardSubtitle}>
                  Melden Sie sich mit Ihren Admin-Zugangsdaten an
                </Text>

                <View style={styles.inputContainer}>
                  <Text style={styles.inputLabel}>E-Mail</Text>
                  <TextInput
                    style={styles.input}
                    placeholder="admin@example.com"
                    placeholderTextColor={COLORS.textDisabled}
                    value={email}
                    onChangeText={setEmail}
                    keyboardType="email-address"
                    autoCapitalize="none"
                    autoCorrect={false}
                  />
                </View>

                <View style={styles.inputContainer}>
                  <Text style={styles.inputLabel}>Passwort</Text>
                  <TextInput
                    style={styles.input}
                    placeholder="••••••••"
                    placeholderTextColor={COLORS.textDisabled}
                    value={password}
                    onChangeText={setPassword}
                    secureTextEntry
                    autoCapitalize="none"
                  />
                </View>

                <TouchableOpacity
                  style={[styles.button, loading && styles.buttonDisabled]}
                  onPress={handleLogin}
                  disabled={loading}
                >
                  {loading ? (
                    <ActivityIndicator color={COLORS.text} />
                  ) : (
                    <Text style={styles.buttonText}>ANMELDEN</Text>
                  )}
                </TouchableOpacity>

                <View style={styles.infoBox}>
                  <Text style={styles.infoText}>
                    ℹ️ Nur autorisiertes Personal hat Zugriff auf diesen Bereich.
                  </Text>
                </View>
              </View>
            </View>
          ) : (
            // Admin Panel
            <View style={styles.adminPanel}>
              <View style={[styles.card, SHADOWS.medium]}>
                <Text style={styles.cardTitle}>ADMIN-PANEL</Text>
                <Text style={styles.cardSubtitle}>
                  Angemeldet als: {user.email}
                </Text>

                <TouchableOpacity
                  style={styles.menuButton}
                  onPress={() => navigation.navigate('UploadMealPlan')}
                >
                  <Text style={styles.menuButtonIcon}>📸</Text>
                  <View style={styles.menuButtonContent}>
                    <Text style={styles.menuButtonTitle}>Speiseplan hochladen</Text>
                    <Text style={styles.menuButtonSubtitle}>
                      Neuen Speiseplan per Kamera hinzufügen
                    </Text>
                  </View>
                  <Text style={styles.menuButtonArrow}>→</Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[styles.menuButton, styles.menuButtonDanger]}
                  onPress={handleLogout}
                >
                  <Text style={styles.menuButtonIcon}>🚪</Text>
                  <View style={styles.menuButtonContent}>
                    <Text style={styles.menuButtonTitle}>Abmelden</Text>
                    <Text style={styles.menuButtonSubtitle}>
                      Aus dem Admin-Bereich abmelden
                    </Text>
                  </View>
                  <Text style={styles.menuButtonArrow}>→</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
        </ScrollView>
      </LinearGradient>
    </KeyboardAvoidingView>
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: COLORS.background,
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
  loginContainer: {
    padding: SIZES.paddingLarge,
  },
  adminPanel: {
    padding: SIZES.paddingLarge,
  },
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radiusLarge,
    padding: SIZES.paddingLarge,
    borderWidth: 2,
    borderColor: COLORS.border,
  },
  cardTitle: {
    ...FONTS.h3,
    color: COLORS.accent,
    fontWeight: '800',
    letterSpacing: 2,
    marginBottom: SIZES.paddingSmall,
  },
  cardSubtitle: {
    ...FONTS.body,
    color: COLORS.textSecondary,
    marginBottom: SIZES.paddingLarge,
  },
  inputContainer: {
    marginBottom: SIZES.padding,
  },
  inputLabel: {
    ...FONTS.bodyBold,
    color: COLORS.text,
    marginBottom: SIZES.paddingSmall,
  },
  input: {
    backgroundColor: COLORS.surfaceLight,
    borderRadius: SIZES.radius,
    padding: SIZES.padding,
    ...FONTS.body,
    color: COLORS.text,
    borderWidth: 2,
    borderColor: COLORS.border,
  },
  button: {
    backgroundColor: COLORS.primary,
    borderRadius: SIZES.radius,
    padding: SIZES.padding,
    alignItems: 'center',
    marginTop: SIZES.padding,
    borderWidth: 2,
    borderColor: COLORS.accent,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    ...FONTS.bodyBold,
    color: COLORS.accent,
    letterSpacing: 1,
  },
  infoBox: {
    backgroundColor: COLORS.primaryDark,
    borderRadius: SIZES.radius,
    padding: SIZES.padding,
    marginTop: SIZES.paddingLarge,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  infoText: {
    ...FONTS.caption,
    color: COLORS.textSecondary,
    lineHeight: 18,
  },
  menuButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.primaryDark,
    borderRadius: SIZES.radiusLarge,
    padding: SIZES.padding,
    marginBottom: SIZES.padding,
    borderWidth: 2,
    borderColor: COLORS.border,
  },
  menuButtonDanger: {
    borderColor: COLORS.danger,
  },
  menuButtonIcon: {
    fontSize: 32,
    marginRight: SIZES.padding,
  },
  menuButtonContent: {
    flex: 1,
  },
  menuButtonTitle: {
    ...FONTS.bodyBold,
    color: COLORS.text,
    marginBottom: 4,
  },
  menuButtonSubtitle: {
    ...FONTS.caption,
    color: COLORS.textSecondary,
  },
  menuButtonArrow: {
    fontSize: 24,
    color: COLORS.accent,
    fontWeight: 'bold',
  },
});

export default AdminScreen;
