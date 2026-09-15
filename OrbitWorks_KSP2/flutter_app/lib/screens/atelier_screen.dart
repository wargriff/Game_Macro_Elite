import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as p;

import '../data/catalog_loader.dart';
import '../models/craft.dart';
import '../services/ksp2_import.dart';
import '../widgets/craft_painter_3d.dart';

class AtelierScreen extends StatefulWidget {
  const AtelierScreen({super.key});

  @override
  State<AtelierScreen> createState() => _AtelierScreenState();
}

class _AtelierScreenState extends State<AtelierScreen> {
  Catalog? _catalog;
  String? _error;
  String _tab = 'all';
  String _destination = 'all';
  String _query = '';
  String _sort = 'name';
  Craft? _selected;
  bool _autoRotate = true;
  bool _importing = false;

  static const tabs = ['all', 'starlink', 'starship', 'rockets', 'rovers', 'comms', 'data'];
  static const labels = {
    'all': 'Tous',
    'starlink': 'Starlink',
    'starship': 'Starship',
    'rockets': 'Fusées',
    'rovers': 'Rovers',
    'comms': 'Comms',
    'data': 'Data',
  };

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final cat = await loadCatalog();
      setState(() {
        _catalog = cat;
        _selected = cat.crafts.isNotEmpty ? cat.crafts.first : null;
      });
    } catch (e) {
      setState(() => _error = e.toString());
    }
  }

  List<Craft> get _filtered {
    final crafts = _catalog?.crafts ?? const <Craft>[];
    var list = crafts.where((c) {
      if (_tab != 'all' && c.category != _tab) return false;
      if (_destination != 'all' && c.destination != _destination) return false;
      if (_query.isEmpty) return true;
      final hay = '${c.name} ${c.category} ${c.id} ${c.destination} ${c.tags.join(' ')}'.toLowerCase();
      return hay.contains(_query.toLowerCase());
    }).toList();

    switch (_sort) {
      case 'mass':
        list.sort((a, b) => b.massT.compareTo(a.massT));
      case 'dv':
        list.sort((a, b) => b.estimatedDvMs.compareTo(a.estimatedDvMs));
      case 'parts':
        list.sort((a, b) => b.partsCount.compareTo(a.partsCount));
      default:
        list.sort((a, b) => a.name.compareTo(b.name));
    }
    return list;
  }

  Future<void> _copyChecklist() async {
    final c = _selected;
    if (c == null) return;
    await Clipboard.setData(ClipboardData(text: c.checklistText));
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Checklist VAB copiée')),
    );
  }

  Future<void> _installToKsp2() async {
    if (kIsWeb) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Import fichier impossible sur le Web. Lance l’app Windows/Linux ou python/install_to_ksp2.py'),
        ),
      );
      return;
    }

    setState(() => _importing = true);
    try {
      // Project root: flutter_app/.. when running from flutter_app
      final root = Directory.current.path.endsWith('flutter_app')
          ? Directory(p.dirname(Directory.current.path))
          : Directory.current;
      final exportDir = Directory(p.join(root.path, 'export'));
      if (!exportDir.existsSync()) {
        throw StateError('Dossier export/ introuvable. Lance: python python/generate_crafts.py');
      }
      final dest = await Ksp2ImportService.installPack(exportDir: exportDir);
      if (!mounted) return;
      await showDialog<void>(
        context: context,
        builder: (ctx) => AlertDialog(
          title: const Text('Pack installé'),
          content: SingleChildScrollView(
            child: Text(
              'Copié dans:\n${dest.path}\n\n'
              '${Ksp2ImportService.note}\n'
              'Ensuite: ouvre un blueprint .md et reconstruis dans le VAB '
              'pour obtenir les VRAIS modèles 3D du jeu.',
            ),
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('OK')),
          ],
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Import échoué: $e')),
      );
    } finally {
      if (mounted) setState(() => _importing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    const bg = Color(0xFF060A12);
    const panel = Color(0xFF0B1422);
    const line = Color(0xFF24344D);
    const accent = Color(0xFF3EC4FF);
    const amber = Color(0xFFF0A33A);

    if (_error != null) {
      return Scaffold(
        backgroundColor: bg,
        body: Center(child: Text(_error!, style: const TextStyle(color: Colors.redAccent))),
      );
    }
    if (_catalog == null) {
      return const Scaffold(
        backgroundColor: bg,
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final filtered = _filtered;
    final destinations = <String>{
      'all',
      ..._catalog!.crafts.map((c) => c.destination).where((d) => d.isNotEmpty),
    }.take(16).toList();

    return Scaffold(
      backgroundColor: bg,
      body: Row(
        children: [
          SizedBox(
            width: 400,
            child: Container(
              decoration: const BoxDecoration(
                color: panel,
                border: Border(right: BorderSide(color: line)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Padding(
                    padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
                    child: Row(
                      children: [
                        Container(
                          width: 46,
                          height: 46,
                          alignment: Alignment.center,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(14),
                            gradient: const LinearGradient(colors: [accent, amber]),
                          ),
                          child: const Text('OW', style: TextStyle(fontWeight: FontWeight.w800, color: Color(0xFF041018))),
                        ),
                        const SizedBox(width: 12),
                        const Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('OrbitWorks', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
                              Text('Flutter · KSP2 · import VAB', style: TextStyle(color: Color(0xFF8AA0BB), fontSize: 12)),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 12),
                    child: Wrap(
                      spacing: 6,
                      runSpacing: 6,
                      children: tabs.map((t) {
                        final n = t == 'all' ? _catalog!.count : (_catalog!.byCategory[t] ?? 0);
                        final selected = _tab == t;
                        return ChoiceChip(
                          label: Text('${labels[t]} ($n)'),
                          selected: selected,
                          onSelected: (_) => setState(() => _tab = t),
                          selectedColor: accent,
                          labelStyle: TextStyle(
                            color: selected ? const Color(0xFF041018) : const Color(0xFF8AA0BB),
                            fontWeight: selected ? FontWeight.w700 : FontWeight.w500,
                            fontSize: 12,
                          ),
                          backgroundColor: const Color(0xFF0A1320),
                        );
                      }).toList(),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.fromLTRB(12, 10, 12, 6),
                    child: TextField(
                      style: const TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        hintText: 'Starship, Starlink, Mun…',
                        hintStyle: const TextStyle(color: Color(0xFF8AA0BB)),
                        filled: true,
                        fillColor: const Color(0xFF070D18),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: const BorderSide(color: line),
                        ),
                        suffixIcon: IconButton(
                          icon: const Icon(Icons.clear, color: Color(0xFF8AA0BB)),
                          onPressed: () => setState(() => _query = ''),
                        ),
                      ),
                      onChanged: (v) => setState(() => _query = v),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 12),
                    child: Row(
                      children: [
                        Expanded(
                          child: DropdownButtonFormField<String>(
                            initialValue: _sort,
                            dropdownColor: const Color(0xFF0A1320),
                            decoration: InputDecoration(
                              filled: true,
                              fillColor: const Color(0xFF070D18),
                              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                            ),
                            items: const [
                              DropdownMenuItem(value: 'name', child: Text('Nom', style: TextStyle(color: Colors.white))),
                              DropdownMenuItem(value: 'mass', child: Text('Masse', style: TextStyle(color: Colors.white))),
                              DropdownMenuItem(value: 'dv', child: Text('Δv', style: TextStyle(color: Colors.white))),
                              DropdownMenuItem(value: 'parts', child: Text('Pièces', style: TextStyle(color: Colors.white))),
                            ],
                            onChanged: (v) => setState(() => _sort = v ?? 'name'),
                          ),
                        ),
                        IconButton(
                          onPressed: filtered.isEmpty
                              ? null
                              : () {
                                  final i = filtered.indexWhere((c) => c.id == _selected?.id);
                                  final n = (i - 1 + filtered.length) % filtered.length;
                                  setState(() => _selected = filtered[n]);
                                },
                          icon: const Icon(Icons.chevron_left, color: Color(0xFF8AA0BB)),
                        ),
                        IconButton(
                          onPressed: filtered.isEmpty
                              ? null
                              : () {
                                  final i = filtered.indexWhere((c) => c.id == _selected?.id);
                                  final n = (i + 1) % filtered.length;
                                  setState(() => _selected = filtered[n]);
                                },
                          icon: const Icon(Icons.chevron_right, color: Color(0xFF8AA0BB)),
                        ),
                      ],
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.fromLTRB(12, 6, 12, 4),
                    child: Wrap(
                      spacing: 6,
                      runSpacing: 6,
                      children: destinations.map((d) {
                        final selected = _destination == d;
                        return FilterChip(
                          label: Text(d == 'all' ? 'Toutes dest.' : d, style: const TextStyle(fontSize: 11)),
                          selected: selected,
                          onSelected: (_) => setState(() => _destination = d),
                          selectedColor: amber.withValues(alpha: 0.35),
                          backgroundColor: const Color(0xFF0A1320),
                          labelStyle: TextStyle(color: selected ? Colors.white : const Color(0xFF8AA0BB)),
                        );
                      }).toList(),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                    child: Text(
                      '${filtered.length} / ${_catalog!.count} appareils',
                      style: const TextStyle(color: Color(0xFF8AA0BB), fontSize: 12),
                    ),
                  ),
                  Expanded(
                    child: ListView.builder(
                      padding: const EdgeInsets.fromLTRB(12, 0, 12, 12),
                      itemCount: filtered.length,
                      itemBuilder: (ctx, i) {
                        final c = filtered[i];
                        final active = c.id == _selected?.id;
                        return InkWell(
                          onTap: () => setState(() => _selected = c),
                          child: Container(
                            margin: const EdgeInsets.only(bottom: 8),
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: active ? accent.withValues(alpha: 0.6) : line),
                              color: active ? accent.withValues(alpha: 0.08) : Colors.white.withValues(alpha: 0.02),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(c.name, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
                                const SizedBox(height: 6),
                                Wrap(
                                  spacing: 6,
                                  children: [
                                    _badge(c.category, accent),
                                    _badge('${c.partsCount} pcs', amber),
                                    _badge('${c.massT.toStringAsFixed(1)} t', const Color(0xFF3DD68C)),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          ),
          Expanded(
            child: Stack(
              children: [
                if (_selected != null)
                  CraftPreview3D(craft: _selected!, autoRotate: _autoRotate)
                else
                  const Center(child: Text('Sélectionne un craft', style: TextStyle(color: Colors.white54))),
                Positioned(
                  top: 14,
                  left: 14,
                  right: 14,
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Flexible(
                        child: Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: const Color(0xCC080E18),
                            borderRadius: BorderRadius.circular(12),
                            border: const Border.fromBorderSide(BorderSide(color: line)),
                          ),
                          child: const Text(
                            'Preview 3D procédurale (pas les meshes propriétaires KSP2). '
                            'Pour les VRAIS modèles: Installe le pack puis reconstruis dans le VAB.',
                            style: TextStyle(color: Color(0xFF8AA0BB), fontSize: 12),
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Wrap(
                        spacing: 6,
                        children: [
                          _ghostBtn(_autoRotate ? 'Auto-rotate ON' : 'Auto-rotate OFF', () {
                            setState(() => _autoRotate = !_autoRotate);
                          }, active: _autoRotate),
                          _ghostBtn(_importing ? 'Import…' : 'Installer dans KSP2', _importing ? null : _installToKsp2),
                          _ghostBtn('Copier checklist', _copyChecklist),
                        ],
                      ),
                    ],
                  ),
                ),
                if (_selected != null)
                  Positioned(
                    left: 18,
                    right: 18,
                    bottom: 18,
                    child: _Hud(craft: _selected!),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _badge(String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: color.withValues(alpha: 0.35)),
        color: color.withValues(alpha: 0.12),
      ),
      child: Text(text, style: TextStyle(color: color, fontSize: 11)),
    );
  }

  Widget _ghostBtn(String label, VoidCallback? onTap, {bool active = false}) {
    return TextButton(
      onPressed: onTap,
      style: TextButton.styleFrom(
        foregroundColor: active ? const Color(0xFF3EC4FF) : const Color(0xFF8AA0BB),
        backgroundColor: const Color(0xCC0A1320),
        side: BorderSide(color: active ? const Color(0xFF3EC4FF) : const Color(0xFF24344D)),
      ),
      child: Text(label),
    );
  }
}

class _Hud extends StatelessWidget {
  final Craft craft;
  const _Hud({required this.craft});

  @override
  Widget build(BuildContext context) {
    final roles = <String, int>{};
    for (final p in craft.parts) {
      final role = p.role.isEmpty ? p.category : p.role;
      roles[role] = (roles[role] ?? 0) + p.qty;
    }
    final roleEntries = roles.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));

    return Container(
      constraints: const BoxConstraints(maxWidth: 680, maxHeight: 320),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xE0080E18),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFF24344D)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(craft.name, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w700)),
          Text(
            '${craft.destination} · ${craft.subtype.isEmpty ? craft.category : craft.subtype} · Δv ~ ${craft.estimatedDvMs} m/s',
            style: const TextStyle(color: Color(0xFF8AA0BB), fontSize: 12),
          ),
          const SizedBox(height: 10),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              _stat('Pièces', '${craft.partsCount}'),
              _stat('Masse', '${craft.massT.toStringAsFixed(2)} t'),
              _stat('Δv', '${craft.estimatedDvMs} m/s'),
              _stat('Cat.', craft.category),
            ],
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 6,
            runSpacing: 6,
            children: roleEntries
                .map((e) => Chip(
                      label: Text('${e.key} · ${e.value}', style: const TextStyle(fontSize: 11)),
                      backgroundColor: const Color(0xFF0A1320),
                      side: const BorderSide(color: Color(0xFF24344D)),
                      labelStyle: const TextStyle(color: Color(0xFF8AA0BB)),
                      visualDensity: VisualDensity.compact,
                    ))
                .toList(),
          ),
          const SizedBox(height: 6),
          const Text('CHECKLIST PIÈCES (NOMS JEU)', style: TextStyle(color: Color(0xFF8AA0BB), fontSize: 11, letterSpacing: 0.6)),
          const SizedBox(height: 6),
          Expanded(
            child: ListView.builder(
              itemCount: craft.parts.length,
              itemBuilder: (_, i) {
                final p = craft.parts[i];
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 3),
                  child: Row(
                    children: [
                      SizedBox(
                        width: 40,
                        child: Text('×${p.qty}', style: const TextStyle(color: Color(0xFFF0A33A), fontWeight: FontWeight.w700)),
                      ),
                      Expanded(child: Text(p.displayName, style: const TextStyle(color: Colors.white70, fontSize: 12))),
                      Text(p.role, style: const TextStyle(color: Color(0xFF8AA0BB), fontSize: 11)),
                    ],
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _stat(String k, String v) {
    return Container(
      width: 110,
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.black26,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: const Color(0xFF24344D)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(k, style: const TextStyle(color: Color(0xFF8AA0BB), fontSize: 11)),
          Text(v, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}
