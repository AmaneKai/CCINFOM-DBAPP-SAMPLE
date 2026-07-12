-- ============================================================
-- CCINFOM DB App Sample — Hotel Management System
-- Seed data script
-- Run this against `hotel_db` AFTER running Django migrations
-- (the tables must already exist: hotel_roomtype, hotel_room,
-- hotel_guest, hotel_staff, hotel_booking)
-- ============================================================

USE hotel_db;

-- Clear existing data (safe to run multiple times during dev)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE hotel_booking;
TRUNCATE TABLE hotel_room;
TRUNCATE TABLE hotel_roomtype;
TRUNCATE TABLE hotel_guest;
TRUNCATE TABLE hotel_staff;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- Room types (rate lives here, not on Room, per 3NF)
-- ============================================================
INSERT INTO hotel_roomtype (type_code, type_name, base_rate) VALUES
('STD', 'Standard', 1500.00),
('DLX', 'Deluxe', 2500.00),
('STE', 'Suite', 4500.00);

-- ============================================================
-- Rooms
-- ============================================================
INSERT INTO hotel_room (room_number, room_type_id, floor, status) VALUES
('101', 'STD', 1, 'available'),
('102', 'STD', 1, 'available'),
('103', 'STD', 1, 'occupied'),
('201', 'DLX', 2, 'available'),
('202', 'DLX', 2, 'reserved'),
('203', 'DLX', 2, 'available'),
('301', 'STE', 3, 'available'),
('302', 'STE', 3, 'occupied'),
('303', 'STE', 3, 'available'),
('304', 'STE', 3, 'available');

-- ============================================================
-- Guests (20 total)
-- ============================================================
INSERT INTO hotel_guest (last_name, first_name, contact_number) VALUES
('Santos', 'Maria', '09171234567'),
('Reyes', 'Juan', '09181234567'),
('Cruz', 'Ana', '09191234567'),
('Garcia', 'Pedro', '09201234567'),
('Torres', 'Sofia', '09211234567'),
('Flores', 'Miguel', '09221234567'),
('Ramos', 'Elena', '09231234567'),
('Diaz', 'Carlos', '09241234567'),
('Mendoza', 'Isabel', '09251234567'),
('Aquino', 'Rafael', '09261234567'),
('Lopez', 'Andres', '09271234567'),
('Fernandez', 'Lucia', '09281234567'),
('Morales', 'Vicente', '09291234567'),
('Ramirez', 'Patricia', '09301234567'),
('Ortiz', 'Emilio', '09311234567'),
('Gutierrez', 'Rosa', '09321234567'),
('Chavez', 'Fernando', '09331234567'),
('Vargas', 'Beatriz', '09341234567'),
('Castillo', 'Hector', '09351234567'),
('Rios', 'Gabriela', '09361234567');

-- ============================================================
-- Staff
-- ============================================================
INSERT INTO hotel_staff (last_name, first_name, position) VALUES
('Bautista', 'Luis', 'Front Desk'),
('Villanueva', 'Carmen', 'Front Desk'),
('Gonzales', 'Ramon', 'Manager'),
('Castro', 'Teresa', 'Front Desk'),
('Navarro', 'Diego', 'Housekeeping');

-- ============================================================
-- Bookings — 2025 (full year, for year-over-year comparisons)
-- ============================================================
INSERT INTO hotel_booking (guest_id, room_id, staff_id, check_in_date, check_out_date, status) VALUES
(1, '101', 1, '2025-01-05', '2025-01-08', 'completed'),
(2, '201', 2, '2025-01-12', '2025-01-14', 'completed'),
(3, '301', 3, '2025-01-20', '2025-01-23', 'completed'),
(4, '102', 1, '2025-02-03', '2025-02-05', 'completed'),
(5, '202', 4, '2025-02-14', '2025-02-16', 'completed'),
(6, '302', 2, '2025-02-22', '2025-02-25', 'completed'),
(7, '103', 1, '2025-03-01', '2025-03-04', 'completed'),
(8, '203', 3, '2025-03-10', '2025-03-12', 'completed'),
(9, '303', 4, '2025-03-18', '2025-03-21', 'completed'),
(10, '304', 2, '2025-03-25', '2025-03-27', 'completed'),
(11, '101', 1, '2025-04-02', '2025-04-05', 'completed'),
(12, '201', 3, '2025-04-11', '2025-04-13', 'completed'),
(13, '301', 4, '2025-04-19', '2025-04-22', 'completed'),
(14, '102', 1, '2025-05-01', '2025-05-03', 'completed'),
(15, '202', 2, '2025-05-09', '2025-05-12', 'completed'),
(16, '302', 3, '2025-05-17', '2025-05-19', 'completed'),
(17, '103', 4, '2025-05-25', '2025-05-28', 'completed'),
(18, '203', 1, '2025-06-02', '2025-06-05', 'completed'),
(19, '303', 2, '2025-06-11', '2025-06-13', 'completed'),
(20, '304', 3, '2025-06-19', '2025-06-22', 'completed'),
(1, '101', 4, '2025-07-01', '2025-07-04', 'completed'),
(2, '201', 1, '2025-07-10', '2025-07-12', 'completed'),
(3, '301', 2, '2025-07-18', '2025-07-21', 'completed'),
(4, '102', 3, '2025-08-05', '2025-08-08', 'completed'),
(5, '202', 4, '2025-08-14', '2025-08-16', 'completed'),
(6, '302', 1, '2025-08-22', '2025-08-25', 'completed'),
(7, '103', 2, '2025-09-01', '2025-09-04', 'completed'),
(8, '203', 3, '2025-09-10', '2025-09-12', 'completed'),
(9, '303', 4, '2025-09-19', '2025-09-22', 'completed'),
(10, '304', 1, '2025-10-02', '2025-10-05', 'completed'),
(11, '101', 2, '2025-10-11', '2025-10-13', 'completed'),
(12, '201', 3, '2025-10-20', '2025-10-23', 'completed'),
(13, '301', 4, '2025-11-03', '2025-11-06', 'completed'),
(14, '102', 1, '2025-11-12', '2025-11-14', 'completed'),
(15, '202', 2, '2025-11-21', '2025-11-24', 'completed'),
(16, '302', 3, '2025-12-05', '2025-12-08', 'completed'),
(17, '103', 4, '2025-12-14', '2025-12-17', 'completed'),
(18, '203', 1, '2025-12-22', '2025-12-26', 'completed'),
(19, '303', 2, '2025-12-28', '2025-12-31', 'completed');

-- ============================================================
-- Bookings — 2026 (Jan–Jul, mix of statuses to show the full
-- transaction lifecycle: reserved -> checked-in -> completed)
-- ============================================================
INSERT INTO hotel_booking (guest_id, room_id, staff_id, check_in_date, check_out_date, status) VALUES
(20, '304', 3, '2026-01-04', '2026-01-07', 'completed'),
(1, '101', 4, '2026-01-15', '2026-01-17', 'completed'),
(2, '201', 1, '2026-01-24', '2026-01-27', 'completed'),
(3, '301', 2, '2026-02-02', '2026-02-05', 'completed'),
(4, '102', 3, '2026-02-11', '2026-02-13', 'completed'),
(5, '202', 4, '2026-02-19', '2026-02-22', 'completed'),
(6, '302', 1, '2026-03-01', '2026-03-04', 'completed'),
(7, '103', 2, '2026-03-10', '2026-03-12', 'completed'),
(8, '203', 3, '2026-03-18', '2026-03-21', 'completed'),
(9, '303', 4, '2026-04-02', '2026-04-05', 'completed'),
(10, '304', 1, '2026-04-11', '2026-04-13', 'completed'),
(11, '101', 2, '2026-04-20', '2026-04-23', 'completed'),
(12, '201', 3, '2026-05-01', '2026-05-04', 'completed'),
(13, '301', 4, '2026-05-10', '2026-05-12', 'completed'),
(14, '102', 1, '2026-05-19', '2026-05-22', 'completed'),
(15, '202', 2, '2026-06-02', '2026-06-05', 'completed'),
(16, '302', 1, '2026-06-11', '2026-06-13', 'checked-in'),
(17, '103', 4, '2026-06-19', '2026-06-22', 'checked-in'),
(18, '203', 2, '2026-06-25', '2026-06-27', 'checked-in'),
(19, '303', 1, '2026-06-28', '2026-06-30', 'completed'),
(20, '304', 3, '2026-07-01', '2026-07-03', 'checked-in'),
(1, '101', 2, '2026-07-05', '2026-07-07', 'reserved'),
(2, '201', 1, '2026-07-10', '2026-07-12', 'reserved'),
(3, '301', 4, '2026-07-15', '2026-07-18', 'reserved');

-- ============================================================
-- Verification queries — run manually to sanity-check counts
-- ============================================================
-- SELECT COUNT(*) FROM hotel_roomtype;   -- expect 3
-- SELECT COUNT(*) FROM hotel_room;       -- expect 10
-- SELECT COUNT(*) FROM hotel_guest;      -- expect 20
-- SELECT COUNT(*) FROM hotel_staff;      -- expect 5
-- SELECT COUNT(*) FROM hotel_booking;    -- expect 61
-- SELECT status, COUNT(*) FROM hotel_booking GROUP BY status;
