class CraftPart {
  final String partId;
  final String displayName;
  final String category;
  final String role;
  final int qty;
  final double massT;

  const CraftPart({
    required this.partId,
    required this.displayName,
    required this.category,
    required this.role,
    required this.qty,
    required this.massT,
  });

  factory CraftPart.fromJson(Map<String, dynamic> j) => CraftPart(
        partId: (j['part_id'] ?? j['partId'] ?? '').toString(),
        displayName: (j['display_name'] ?? j['displayName'] ?? '').toString(),
        category: (j['category'] ?? '').toString(),
        role: (j['role'] ?? '').toString(),
        qty: (j['qty'] as num?)?.toInt() ?? 1,
        massT: (j['mass_t'] as num?)?.toDouble() ?? 0,
      );
}

class Craft {
  final String id;
  final String name;
  final String category;
  final String type;
  final String subtype;
  final String preview;
  final String destination;
  final List<String> tags;
  final String notes;
  final int partsCount;
  final double massT;
  final int estimatedDvMs;
  final String blueprintFile;
  final String vesselFile;
  final List<CraftPart> parts;

  const Craft({
    required this.id,
    required this.name,
    required this.category,
    required this.type,
    required this.subtype,
    required this.preview,
    required this.destination,
    required this.tags,
    required this.notes,
    required this.partsCount,
    required this.massT,
    required this.estimatedDvMs,
    required this.blueprintFile,
    required this.vesselFile,
    required this.parts,
  });

  factory Craft.fromJson(Map<String, dynamic> j) => Craft(
        id: (j['id'] ?? '').toString(),
        name: (j['name'] ?? '').toString(),
        category: (j['category'] ?? '').toString(),
        type: (j['type'] ?? '').toString(),
        subtype: (j['subtype'] ?? '').toString(),
        preview: (j['preview'] ?? j['category'] ?? '').toString(),
        destination: (j['destination'] ?? '').toString(),
        tags: ((j['tags'] as List?) ?? const []).map((e) => e.toString()).toList(),
        notes: (j['notes'] ?? '').toString(),
        partsCount: (j['parts_count'] as num?)?.toInt() ?? 0,
        massT: (j['mass_t'] as num?)?.toDouble() ?? 0,
        estimatedDvMs: (j['estimated_dv_ms'] as num?)?.toInt() ?? 0,
        blueprintFile: (j['blueprint_file'] ?? '').toString(),
        vesselFile: (j['vessel_file'] ?? '').toString(),
        parts: ((j['parts'] as List?) ?? const [])
            .map((e) => CraftPart.fromJson(Map<String, dynamic>.from(e as Map)))
            .toList(),
      );

  String get checklistText {
    final buf = StringBuffer()
      ..writeln('# $name')
      ..writeln('Destination: $destination')
      ..writeln('Δv ~ $estimatedDvMs m/s')
      ..writeln()
      ..writeln('Checklist VAB (noms jeu):');
    for (final p in parts) {
      buf.writeln('- [ ] ×${p.qty}  ${p.displayName}');
    }
    return buf.toString();
  }
}

class Catalog {
  final int count;
  final Map<String, int> byCategory;
  final List<Craft> crafts;
  final String note;

  const Catalog({
    required this.count,
    required this.byCategory,
    required this.crafts,
    required this.note,
  });

  factory Catalog.fromJson(Map<String, dynamic> j) => Catalog(
        count: (j['count'] as num?)?.toInt() ?? 0,
        byCategory: Map<String, int>.from(
          (j['by_category'] as Map? ?? {}).map(
            (k, v) => MapEntry(k.toString(), (v as num).toInt()),
          ),
        ),
        crafts: ((j['crafts'] as List?) ?? const [])
            .map((e) => Craft.fromJson(Map<String, dynamic>.from(e as Map)))
            .toList(),
        note: (j['ksp2_note'] ?? '').toString(),
      );
}
