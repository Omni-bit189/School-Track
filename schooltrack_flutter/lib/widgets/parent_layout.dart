import 'package:flutter/material.dart';
import '../core/theme.dart';
import 'base_layout.dart';

class ParentLayout extends StatelessWidget {
  final Widget child;
  const ParentLayout({super.key, required this.child});

  @override
  Widget build(BuildContext context) => BaseLayout(
        child: child,
        accentColor: Colors.orange,
        settingsPath: '/parent/settings',
        navItems: const [
          NavItem(Icons.person_outline, 'My Dashboard', '/parent/dashboard'),
          NavItem(Icons.people_outline, 'Children', '/parent/children'),
          NavItem(Icons.grade_outlined, 'Results', '/parent/results'),
          NavItem(Icons.settings_outlined, 'Settings', '/parent/settings'),
        ],
      );
}
