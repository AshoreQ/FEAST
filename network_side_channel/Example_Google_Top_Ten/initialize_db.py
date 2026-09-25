#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3

OBJECTS_DB = sys.argv[1]

DB_CONN = sqlite3.connect(OBJECTS_DB)
DB_CUR = DB_CONN.cursor()

DB_CUR.execute("CREATE TABLE object_size_map (obj_size real, obj_label text, chunk_index real)")
DB_CUR.execute("CREATE TABLE total_chunk_map (chunk_count real, obj_label text)")

DB_CONN.commit()
