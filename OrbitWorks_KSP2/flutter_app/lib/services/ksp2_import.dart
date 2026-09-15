import 'dart:io';
import 'dart:math' as math;

import 'package:flutter/foundation.dart';
import 'package:path/path.dart' as p;

/// Honest KSP2 import helper.
///
/// KSP2 has no stable official craft import like KSP1.
/// This copies OrbitWorks blueprints + experimental vessel scaffolds into
/// the user's LocalLow OrbitWorks_Import folder so they can rebuild in VAB
/// with stock part display names (real game meshes).
class Ksp2ImportService {
  static const note = '''
KSP2 n'importe PAS les crafts en 1 clic comme KSP1.

OrbitWorks copie :
• Blueprints/*.md  → checklist VAB (noms de pièces stock du jeu)
• Vehicles/*.json  → scaffolds expérimentaux (pas un craft natif)

Les meshes 3D du jeu restent dans TON installation KSP2.
La preview Flutter est une reconstruction procédurale (légal).
''';

  static List<Directory> candidateRoots() {
    final home = Platform.environment['USERPROFILE'] ??
        Platform.environment['HOME'] ??
        '';
    if (home.isEmpty) return const [];
    return [
      Directory(p.join(home, 'AppData', 'LocalLow', 'Intercept Games', 'Kerbal Space Program 2')),
      Directory(p.join(home, 'AppData', 'LocalLow', 'Private Division', 'Kerbal Space Program 2')),
      Directory(p.join(home, '.config', 'unity3d', 'Intercept Games', 'Kerbal Space Program 2')),
    ];
  }

  static Directory? detectExistingRoot() {
    for (final d in candidateRoots()) {
      if (d.existsSync()) return d;
    }
    return null;
  }

  /// Copies export pack into ksp2Root/OrbitWorks_Import
  static Future<Directory> installPack({
    required Directory exportDir,
    Directory? ksp2Root,
  }) async {
    final root = ksp2Root ?? detectExistingRoot() ?? candidateRoots().first;
    final dest = Directory(p.join(root.path, 'OrbitWorks_Import'));
    if (dest.existsSync()) {
      await dest.delete(recursive: true);
    }
    await dest.create(recursive: true);

    final blueprints = Directory(p.join(exportDir.path, 'Blueprints'));
    final vehiclesPack = Directory(p.join(exportDir.path, 'Vehicles', 'KSP2_ImportPack'));
    final vehicles = Directory(p.join(exportDir.path, 'Vehicles'));
    final manifest = File(p.join(exportDir.path, 'orbitworks_manifest.json'));

    if (!blueprints.existsSync()) {
      throw StateError('Blueprints manquants. Lance python/generate_crafts.py');
    }

    await _copyDir(blueprints, Directory(p.join(dest.path, 'Blueprints')));
    if (vehiclesPack.existsSync()) {
      await _copyDir(vehiclesPack, Directory(p.join(dest.path, 'Vehicles')));
    } else if (vehicles.existsSync()) {
      await _copyDir(vehicles, Directory(p.join(dest.path, 'Vehicles')));
    }
    if (manifest.existsSync()) {
      await manifest.copy(p.join(dest.path, 'orbitworks_manifest.json'));
    }

    await File(p.join(dest.path, 'LISEZMOI.txt')).writeAsString(
      'OrbitWorks → KSP2\n\n'
      '$note\n'
      'Étapes:\n'
      '1) Ouvre un blueprint .md\n'
      '2) Dans le VAB, cherche chaque nom affiché\n'
      '3) Assemble bas → haut\n'
      '4) Sauvegarde le véhicule DANS KSP2\n',
    );
    return dest;
  }

  static Future<void> _copyDir(Directory src, Directory dest) async {
    await dest.create(recursive: true);
    await for (final entity in src.list(recursive: true)) {
      final rel = p.relative(entity.path, from: src.path);
      final out = p.join(dest.path, rel);
      if (entity is Directory) {
        await Directory(out).create(recursive: true);
      } else if (entity is File) {
        await File(out).parent.create(recursive: true);
        await entity.copy(out);
      }
    }
  }

  static bool get canWriteFilesystem => !kIsWeb;

  static String defaultExportHint(String projectRoot) =>
      p.normalize(p.join(projectRoot, 'export'));
}

double clamp01(double v) => math.max(0, math.min(1, v));
