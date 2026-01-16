import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { COLORS, SIZES, FONTS, SHADOWS } from '../theme';
import { db } from '../firebase.config';
import { collection, query, where, getDocs, orderBy } from 'firebase/firestore';

const { width } = Dimensions.get('window');

const HomeScreen = ({ navigation }) => {
  const [currentWeek, setCurrentWeek] = useState(null);
  const [mealPlan, setMealPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [weekNumber, setWeekNumber] = useState(0);
  const [year, setYear] = useState(0);

  // Kalenderwoche berechnen
  const getWeekNumber = (date) => {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);
    d.setDate(d.getDate() + 3 - ((d.getDay() + 6) % 7));
    const week1 = new Date(d.getFullYear(), 0, 4);
    const weekNum = 1 + Math.round(((d - week1) / 86400000 - 3 + ((week1.getDay() + 6) % 7)) / 7);
    return { week: weekNum, year: d.getFullYear() };
  };

  // Speiseplan laden
  const loadMealPlan = async (week, year) => {
    try {
      setLoading(true);
      const q = query(
        collection(db, 'mealPlans'),
        where('week', '==', week),
        where('year', '==', year),
        orderBy('createdAt', 'desc')
      );

      const querySnapshot = await getDocs(q);
      if (!querySnapshot.empty) {
        const doc = querySnapshot.docs[0];
        setMealPlan({ id: doc.id, ...doc.data() });
      } else {
        setMealPlan(null);
      }
    } catch (error) {
      console.error('Fehler beim Laden des Speiseplans:', error);
      setMealPlan(null);
    } finally {
      setLoading(false);
    }
  };

  // Initial laden
  useEffect(() => {
    const { week, year } = getWeekNumber(new Date());
    setWeekNumber(week);
    setYear(year);
    loadMealPlan(week, year);
  }, []);

  // Woche wechseln
  const changeWeek = (direction) => {
    const newDate = new Date();
    newDate.setDate(newDate.getDate() + (direction * 7));
    const { week, year } = getWeekNumber(newDate);
    setWeekNumber(week);
    setYear(year);
    loadMealPlan(week, year);
  };

  // Datumsbereich für die Woche berechnen
  const getWeekDateRange = (week, year) => {
    const simple = new Date(year, 0, 1 + (week - 1) * 7);
    const dow = simple.getDay();
    const ISOweekStart = simple;
    if (dow <= 4) ISOweekStart.setDate(simple.getDate() - simple.getDay() + 1);
    else ISOweekStart.setDate(simple.getDate() + 8 - simple.getDay());

    const endDate = new Date(ISOweekStart);
    endDate.setDate(endDate.getDate() + 6);

    const formatDate = (date) => {
      return `${date.getDate()}.${date.getMonth() + 1}.`;
    };

    return `${formatDate(ISOweekStart)} - ${formatDate(endDate)}`;
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={[COLORS.primaryDark, COLORS.background]}
        style={styles.gradient}
      >
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.headerContent}>
            <Text style={styles.headerTitle}>SPEISEPLAN</Text>
            <Text style={styles.headerSubtitle}>Militärische Verpflegung</Text>
          </View>
          <TouchableOpacity
            style={styles.adminButton}
            onPress={() => navigation.navigate('Admin')}
          >
            <Text style={styles.adminButtonText}>⚙️</Text>
          </TouchableOpacity>
        </View>

        {/* Wochen-Navigation */}
        <View style={styles.weekNavigation}>
          <TouchableOpacity
            style={styles.navButton}
            onPress={() => changeWeek(-1)}
          >
            <Text style={styles.navButtonText}>◀</Text>
          </TouchableOpacity>

          <View style={styles.weekInfo}>
            <Text style={styles.weekNumber}>KW {weekNumber}</Text>
            <Text style={styles.weekYear}>{year}</Text>
            <Text style={styles.weekRange}>{getWeekDateRange(weekNumber, year)}</Text>
          </View>

          <TouchableOpacity
            style={styles.navButton}
            onPress={() => changeWeek(1)}
          >
            <Text style={styles.navButtonText}>▶</Text>
          </TouchableOpacity>
        </View>

        {/* Content */}
        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          {loading ? (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color={COLORS.accent} />
              <Text style={styles.loadingText}>Laden...</Text>
            </View>
          ) : mealPlan && mealPlan.imageUrl ? (
            <View style={styles.mealPlanContainer}>
              <View style={[styles.card, SHADOWS.medium]}>
                <Image
                  source={{ uri: mealPlan.imageUrl }}
                  style={styles.mealPlanImage}
                  resizeMode="contain"
                />
                {mealPlan.notes && (
                  <View style={styles.notesContainer}>
                    <Text style={styles.notesLabel}>Hinweise:</Text>
                    <Text style={styles.notesText}>{mealPlan.notes}</Text>
                  </View>
                )}
              </View>
            </View>
          ) : (
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyIcon}>📋</Text>
              <Text style={styles.emptyTitle}>Kein Speiseplan verfügbar</Text>
              <Text style={styles.emptyText}>
                Für diese Woche wurde noch kein Speiseplan hochgeladen.
              </Text>
            </View>
          )}

          {/* Platzhalter für AdMob Banner */}
          <View style={styles.adContainer}>
            <Text style={styles.adPlaceholder}>[ Werbebanner ]</Text>
          </View>
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
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 50,
    paddingHorizontal: SIZES.padding,
    paddingBottom: SIZES.paddingLarge,
    borderBottomWidth: 2,
    borderBottomColor: COLORS.accent,
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
  adminButton: {
    width: 44,
    height: 44,
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radius,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  adminButtonText: {
    fontSize: 24,
  },
  weekNavigation: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: SIZES.padding,
    paddingVertical: SIZES.paddingLarge,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  navButton: {
    width: 50,
    height: 50,
    backgroundColor: COLORS.primary,
    borderRadius: SIZES.radius,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 2,
    borderColor: COLORS.accent,
  },
  navButtonText: {
    fontSize: 20,
    color: COLORS.accent,
    fontWeight: 'bold',
  },
  weekInfo: {
    alignItems: 'center',
    flex: 1,
  },
  weekNumber: {
    ...FONTS.h2,
    color: COLORS.accent,
    fontWeight: '800',
    letterSpacing: 2,
  },
  weekYear: {
    ...FONTS.body,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  weekRange: {
    ...FONTS.caption,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  content: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 100,
  },
  loadingText: {
    ...FONTS.body,
    color: COLORS.textSecondary,
    marginTop: SIZES.padding,
  },
  mealPlanContainer: {
    padding: SIZES.padding,
  },
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radiusLarge,
    overflow: 'hidden',
    borderWidth: 2,
    borderColor: COLORS.border,
  },
  mealPlanImage: {
    width: '100%',
    height: 500,
    backgroundColor: COLORS.surfaceLight,
  },
  notesContainer: {
    padding: SIZES.padding,
    backgroundColor: COLORS.primaryDark,
    borderTopWidth: 2,
    borderTopColor: COLORS.accent,
  },
  notesLabel: {
    ...FONTS.bodyBold,
    color: COLORS.accent,
    marginBottom: 8,
  },
  notesText: {
    ...FONTS.body,
    color: COLORS.text,
    lineHeight: 22,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 100,
    paddingHorizontal: SIZES.paddingLarge,
  },
  emptyIcon: {
    fontSize: 64,
    marginBottom: SIZES.padding,
  },
  emptyTitle: {
    ...FONTS.h3,
    color: COLORS.text,
    marginBottom: SIZES.paddingSmall,
    textAlign: 'center',
  },
  emptyText: {
    ...FONTS.body,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  adContainer: {
    height: 80,
    backgroundColor: COLORS.surfaceLight,
    margin: SIZES.padding,
    borderRadius: SIZES.radius,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: COLORS.border,
    borderStyle: 'dashed',
  },
  adPlaceholder: {
    ...FONTS.caption,
    color: COLORS.textSecondary,
  },
});

export default HomeScreen;
