import 'package:flutter/material.dart';

import 'screens/atelier_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const OrbitWorksApp());
}

class OrbitWorksApp extends StatelessWidget {
  const OrbitWorksApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OrbitWorks KSP2',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF3EC4FF),
          secondary: Color(0xFFF0A33A),
          surface: Color(0xFF0B1422),
        ),
        scaffoldBackgroundColor: const Color(0xFF060A12),
        useMaterial3: true,
      ),
      home: const AtelierScreen(),
    );
  }
}
