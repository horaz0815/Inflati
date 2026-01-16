import React from 'react';
import { View, Text, StyleSheet, Platform } from 'react-native';
import { COLORS, SIZES, FONTS } from '../theme';

// WICHTIG: Für die Verwendung von Google AdMob:
// 1. Installieren Sie: npm install react-native-google-mobile-ads
// 2. Registrieren Sie Ihre App bei Google AdMob
// 3. Ersetzen Sie die Platzhalter-IDs unten mit Ihren echten AdMob-IDs
// 4. Uncomment die unten stehende Implementierung

/*
import { BannerAd, BannerAdSize, TestIds } from 'react-native-google-mobile-ads';

// AdMob Banner IDs (Ersetzen Sie diese mit Ihren echten IDs aus AdMob)
const ADMOB_BANNER_ID = Platform.select({
  ios: 'ca-app-pub-xxxxxxxxxxxxx/yyyyyyyyyy', // Ihre iOS Banner ID
  android: 'ca-app-pub-xxxxxxxxxxxxx/yyyyyyyyyy', // Ihre Android Banner ID
});

// Verwenden Sie Test IDs während der Entwicklung
const BANNER_ID = __DEV__ ? TestIds.BANNER : ADMOB_BANNER_ID;
*/

const AdBanner = ({ style }) => {
  // Temporäre Platzhalter-Komponente
  // Ersetzen Sie diese mit der echten AdMob-Implementierung
  return (
    <View style={[styles.container, style]}>
      <View style={styles.placeholder}>
        <Text style={styles.placeholderText}>Google AdMob Banner</Text>
        <Text style={styles.placeholderSubtext}>
          Konfigurieren Sie AdMob in dieser Datei
        </Text>
      </View>
    </View>
  );

  /*
  // ECHTE ADMOB IMPLEMENTIERUNG (Uncomment nach der Konfiguration)
  return (
    <View style={[styles.container, style]}>
      <BannerAd
        unitId={BANNER_ID}
        size={BannerAdSize.BANNER}
        requestOptions={{
          requestNonPersonalizedAdsOnly: false,
        }}
        onAdLoaded={() => {
          console.log('Banner Ad geladen');
        }}
        onAdFailedToLoad={(error) => {
          console.log('Banner Ad Fehler:', error);
        }}
      />
    </View>
  );
  */
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    marginVertical: SIZES.padding,
  },
  placeholder: {
    height: 50,
    width: 320,
    backgroundColor: COLORS.surfaceLight,
    borderRadius: SIZES.radius,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
    borderStyle: 'dashed',
  },
  placeholderText: {
    ...FONTS.caption,
    color: COLORS.textSecondary,
    fontWeight: 'bold',
  },
  placeholderSubtext: {
    ...FONTS.caption,
    color: COLORS.textDisabled,
    fontSize: 10,
    marginTop: 4,
  },
});

export default AdBanner;
