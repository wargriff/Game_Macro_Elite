import 'dart:convert';

import 'package:flutter/services.dart';

import '../models/craft.dart';

Future<Catalog> loadCatalog() async {
  final raw = await rootBundle.loadString('assets/catalog.json');
  final json = jsonDecode(raw) as Map<String, dynamic>;
  return Catalog.fromJson(json);
}
