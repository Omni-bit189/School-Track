import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import '../core/theme.dart';
import '../core/auth_provider.dart';
import '../core/theme_provider.dart';

class NavItem {
  final IconData icon;
  final String label;
  final String path;
  const NavItem(this.icon, this.label, this.path);
}

class BaseLayout extends StatelessWidget {
  final Widget child;
  final List<NavItem> navItems;
  final String settingsPath;
  final Color accentColor;

  const BaseLayout({
    super.key,
    required this.child,
    required this.navItems,
    required this.settingsPath,
    this.accentColor = AppTheme.primary,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          _Sidebar(
            navItems: navItems,
            settingsPath: settingsPath,
            accentColor: accentColor,
          ),
          Expanded(
            child: Column(
              children: [
                _TopBar(accentColor: accentColor),
                Expanded(child: child),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _Sidebar extends StatelessWidget {
  final List<NavItem> navItems;
  final String settingsPath;
  final Color accentColor;

  const _Sidebar({
    required this.navItems,
    required this.settingsPath,
    required this.accentColor,
  });

  @override
  Widget build(BuildContext context) {
    final location = GoRouterState.of(context).matchedLocation;
    final isDark = context.watch<ThemeProvider>().isDark;
    final sidebarBg = isDark ? AppTheme.darkSidebar : AppTheme.sidebar;

    return Container(
      width: 220,
      color: sidebarBg,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Logo + role badge
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 24, 20, 20),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: accentColor,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child:
                      const Icon(Icons.school, color: Colors.white, size: 18),
                ),
                const SizedBox(width: 10),
                const Text('SchoolTrack',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 15,
                        fontWeight: FontWeight.w700)),
              ],
            ),
          ),
          const Divider(color: Colors.white12, height: 1),
          const SizedBox(height: 12),

          ...navItems.map((item) => _NavTile(
                item: item,
                current: location,
                accentColor: accentColor,
              )),

          const Spacer(),
          const Divider(color: Colors.white12, height: 1),
          const SizedBox(height: 8),

          // Settings
          _NavTile(
            item: NavItem(Icons.settings_outlined, 'Settings', settingsPath),
            current: location,
            accentColor: accentColor,
          ),

          // Logout
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            child: InkWell(
              borderRadius: BorderRadius.circular(8),
              onTap: () => _confirmLogout(context),
              child: Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                child: const Row(
                  children: [
                    Icon(Icons.logout, size: 18, color: Colors.white54),
                    SizedBox(width: 12),
                    Text('Logout',
                        style: TextStyle(color: Colors.white70, fontSize: 14)),
                  ],
                ),
              ),
            ),
          ),
          const SizedBox(height: 12),
        ],
      ),
    );
  }

  Future<void> _confirmLogout(BuildContext context) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Log out'),
        content: const Text('Are you sure you want to log out?'),
        actions: [
          TextButton(
              onPressed: () => Navigator.pop(ctx, false),
              child: const Text('Cancel')),
          ElevatedButton(
              onPressed: () => Navigator.pop(ctx, true),
              style: ElevatedButton.styleFrom(backgroundColor: AppTheme.danger),
              child: const Text('Log out')),
        ],
      ),
    );
    if (confirmed == true && context.mounted) {
      await context.read<AuthProvider>().logout();
      if (context.mounted) context.go('/login');
    }
  }
}

class _NavTile extends StatelessWidget {
  final NavItem item;
  final String current;
  final Color accentColor;

  const _NavTile({
    required this.item,
    required this.current,
    required this.accentColor,
  });

  @override
  Widget build(BuildContext context) {
    final isActive = current.startsWith(item.path);
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 2),
      child: InkWell(
        borderRadius: BorderRadius.circular(8),
        onTap: () => context.go(item.path),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
          decoration: BoxDecoration(
            color: isActive
                ? accentColor.withValues(alpha: 0.15)
                : Colors.transparent,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Row(
            children: [
              Icon(item.icon,
                  size: 18, color: isActive ? accentColor : Colors.white54),
              const SizedBox(width: 12),
              Text(item.label,
                  style: TextStyle(
                      color: isActive ? Colors.white : Colors.white70,
                      fontSize: 14,
                      fontWeight:
                          isActive ? FontWeight.w600 : FontWeight.w400)),
            ],
          ),
        ),
      ),
    );
  }
}

class _TopBar extends StatelessWidget {
  final Color accentColor;
  const _TopBar({required this.accentColor});

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final themeProvider = context.watch<ThemeProvider>();
    final isDark = themeProvider.isDark;
    final location = GoRouterState.of(context).matchedLocation;

    final titles = {
      '/admin/dashboard': 'Dashboard',
      '/admin/users': 'User Management',
      '/admin/school': 'School Settings',
      '/admin/settings': 'Settings',
      '/teacher/dashboard': 'My Dashboard',
      '/teacher/attendance': 'Attendance',
      '/teacher/results': 'Results',
      '/teacher/settings': 'Settings',
      '/mentor/dashboard': 'My Mentees',
      '/mentor/settings': 'Settings',
      '/student/dashboard': 'My Dashboard',
      '/student/settings': 'Settings',
      '/parent/dashboard': 'My Dashboard',
      '/parent/children': 'Children',
      '/parent/results': 'Results',
      '/parent/settings': 'Settings',
    };

    String title = 'SchoolTrack';
    titles.forEach((path, t) {
      if (location.startsWith(path)) title = t;
    });
    if (location.startsWith('/mentor/mentee/')) title = 'Mentee Record';

    return Container(
      height: 64,
      padding: const EdgeInsets.symmetric(horizontal: 24),
      decoration: BoxDecoration(
        color: isDark ? AppTheme.darkSurface : AppTheme.surface,
        border: Border(
            bottom: BorderSide(
                color: isDark ? AppTheme.darkBorder : AppTheme.border)),
      ),
      child: Row(
        children: [
          Text(title,
              style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                  color: isDark
                      ? AppTheme.darkTextPrimary
                      : AppTheme.textPrimary)),
          const Spacer(),

          // Role badge
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              color: accentColor.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: accentColor.withValues(alpha: 0.3)),
            ),
            child: Text(
              auth.role?.replaceAll('_', ' ').toUpperCase() ?? '',
              style: TextStyle(
                  fontSize: 10,
                  fontWeight: FontWeight.w700,
                  color: accentColor),
            ),
          ),
          const SizedBox(width: 12),

          // Theme toggle
          IconButton(
            tooltip: isDark ? 'Light Mode' : 'Dark Mode',
            onPressed: () => themeProvider.toggle(),
            style: IconButton.styleFrom(
              backgroundColor:
                  isDark ? AppTheme.darkBackground : AppTheme.background,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                  side: BorderSide(
                      color: isDark ? AppTheme.darkBorder : AppTheme.border)),
            ),
            icon: Icon(
              isDark ? Icons.light_mode : Icons.dark_mode,
              size: 18,
              color: isDark ? Colors.amber : accentColor,
            ),
          ),
          const SizedBox(width: 8),

          // User chip
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: isDark ? AppTheme.darkBackground : AppTheme.background,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(
                  color: isDark ? AppTheme.darkBorder : AppTheme.border),
            ),
            child: Row(
              children: [
                CircleAvatar(
                  radius: 14,
                  backgroundColor: accentColor,
                  child:
                      const Icon(Icons.person, size: 16, color: Colors.white),
                ),
                const SizedBox(width: 8),
                Text(auth.userName ?? 'User',
                    style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w500,
                        color: isDark
                            ? AppTheme.darkTextPrimary
                            : AppTheme.textPrimary)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
