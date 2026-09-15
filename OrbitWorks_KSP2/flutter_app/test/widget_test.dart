import 'package:flutter_test/flutter_test.dart';
import 'package:orbitworks_ksp2/main.dart';

void main() {
  testWidgets('OrbitWorks app boots', (tester) async {
    await tester.pumpWidget(const OrbitWorksApp());
    await tester.pump(const Duration(milliseconds: 100));
    expect(find.textContaining('OrbitWorks'), findsWidgets);
  });
}
