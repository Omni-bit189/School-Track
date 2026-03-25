import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import '../core/auth_provider.dart';
import '../screens/login_screen.dart';
import '../screens/settings_screen.dart';
import '../screens/admin/admin_dashboard.dart';
import '../screens/admin/users_screen.dart';
import '../screens/admin/school_settings_screen.dart';
import '../screens/teacher/teacher_dashboard.dart';
import '../screens/teacher/attendance_screen.dart';
import '../screens/teacher/results_screen.dart';
import '../screens/mentor/mentor_dashboard.dart';
import '../screens/mentor/mentee_detail_screen.dart';
import '../screens/student/student_dashboard.dart';
import '../screens/students_screen.dart';
import '../screens/results_screen.dart';
import '../screens/parent_dashboard.dart';
import '../widgets/admin_layout.dart';
import '../widgets/teacher_layout.dart';
import '../widgets/mentor_layout.dart';
import '../widgets/student_layout.dart';
import '../widgets/parent_layout.dart';

GoRouter createRouter(AuthProvider authProvider) {
  return GoRouter(
    initialLocation: '/login',
    refreshListenable: authProvider,
    redirect: (context, state) {
      final isAuth = authProvider.isAuthenticated;
      final isLoginPage = state.matchedLocation == '/login';
      final role = authProvider.role;

      if (!isAuth && !isLoginPage) return '/login';
      if (isAuth && isLoginPage) {
        // Redirect to role-specific home
        switch (role) {
          case 'school_admin':
          case 'super_admin':
            return '/admin/dashboard';
          case 'teacher':
            return '/teacher/dashboard';
          case 'mentor':
            return '/mentor/dashboard';
          case 'student':
            return '/student/dashboard';
          case 'parent':
            return '/parent/dashboard';
          default:
            return '/admin/dashboard';
        }
      }
      return null;
    },
    routes: [
      GoRoute(path: '/login', builder: (_, __) => const LoginScreen()),

      // ── Admin ─────────────────────────────────────────────
      ShellRoute(
        builder: (context, state, child) => AdminLayout(child: child),
        routes: [
          GoRoute(
              path: '/admin/dashboard',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: AdminDashboard())),
          GoRoute(
              path: '/admin/users',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: UsersScreen())),
          GoRoute(
              path: '/admin/school',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: SchoolSettingsScreen())),
          GoRoute(
              path: '/admin/settings',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: SettingsScreen())),
        ],
      ),

      // ── Teacher ───────────────────────────────────────────
      ShellRoute(
        builder: (context, state, child) => TeacherLayout(child: child),
        routes: [
          GoRoute(
              path: '/teacher/dashboard',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: TeacherDashboard())),
          GoRoute(
              path: '/teacher/attendance',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: TeacherAttendanceScreen())),
          GoRoute(
              path: '/teacher/results',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: TeacherResultsScreen())),
          GoRoute(
              path: '/teacher/settings',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: SettingsScreen())),
        ],
      ),

      // ── Mentor ────────────────────────────────────────────
      ShellRoute(
        builder: (context, state, child) => MentorLayout(child: child),
        routes: [
          GoRoute(
              path: '/mentor/dashboard',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: MentorDashboard())),
          GoRoute(
              path: '/mentor/mentee/:id',
              pageBuilder: (context, state) => NoTransitionPage(
                  child: MenteeDetailScreen(
                      studentId: int.parse(state.pathParameters['id']!)))),
          GoRoute(
              path: '/mentor/settings',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: SettingsScreen())),
        ],
      ),

      // ── Student ───────────────────────────────────────────
      ShellRoute(
        builder: (context, state, child) => StudentLayout(child: child),
        routes: [
          GoRoute(
              path: '/student/dashboard',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: StudentDashboard())),
          GoRoute(
              path: '/student/settings',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: SettingsScreen())),
        ],
      ),

      // ── Parent ────────────────────────────────────────────
      ShellRoute(
        builder: (context, state, child) => ParentLayout(child: child),
        routes: [
          GoRoute(
              path: '/parent/dashboard',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: ParentDashboard())),
          GoRoute(
              path: '/parent/children',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: StudentsScreen())),
          GoRoute(
              path: '/parent/results',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: ResultsScreen())),
          GoRoute(
              path: '/parent/settings',
              pageBuilder: (_, __) =>
                  const NoTransitionPage(child: SettingsScreen())),
        ],
      ),
    ],
  );
}
