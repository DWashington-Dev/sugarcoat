# Design System Specification: Clinical Etherealism

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Digital Sanctuary."** In the high-stakes world of health tech, we move away from the "clinical coldness" of traditional medical software. Instead, we embrace a high-end editorial aesthetic that feels breathable, supportive, and meticulously curated.

To break the "template" look, we reject rigid grids in favor of **Intentional Asymmetry**. Large `display-lg` typography should be paired with expansive whitespace, allowing content to "float" rather than be boxed in. By layering semi-transparent surfaces and utilizing radical border radii, we create an interface that feels less like a computer program and more like a high-end wellness publication.

---

## 2. Color Strategy & Tonal Architecture
The palette is rooted in high-chroma blues and pristine neutrals, designed to evoke clarity and calm.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders for sectioning or layout containment. Structural boundaries must be defined solely through background color shifts. For example, a `surface-container-low` section should sit directly on a `surface` background to create a soft, edge-less transition.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers—like stacked sheets of frosted glass.
*   **Base:** `surface` (#f5f6f7) for the primary application background.
*   **Secondary Layer:** `surface-container-low` (#eff1f2) for large content areas.
*   **The "Pop" Layer:** `surface-container-lowest` (#ffffff) for the highest-priority cards or interactive elements, providing a natural "lift" without the need for heavy shadows.

### Signature Textures & Glass
To achieve the premium aesthetic, use **Glassmorphism** for floating elements (modals, navigation bars).
*   **Glass Token:** Use `surface` at 70% opacity with a `backdrop-blur` of 20px–40px.
*   **Gradients:** Use a subtle linear gradient (Top-Left to Bottom-Right) transitioning from `primary` (#005f98) to `primary_container` (#2aa7ff) for primary CTAs to add "soul" and depth.

---

## 3. Typography: The Editorial Voice
We utilize **Plus Jakarta Sans** for its approachable, geometric clarity. The goal is a high-contrast hierarchy that guides the eye effortlessly.

*   **Display (lg/md/sm):** Reserved for hero health metrics or welcoming headers. Use `on_surface` with `-0.02em` letter spacing to feel tight and professional.
*   **Headlines:** Used for section titles. Ensure generous `margin-bottom` (token `8` or `10`) to maintain the "airy" feel.
*   **Body (lg/md):** Our primary data-reading font. Use `on_surface_variant` for secondary information to create a soft gray-scale contrast against the high-chroma blue accents.
*   **Labels:** Small, all-caps, or high-weight markers for data points. These should use `primary` color to draw attention without adding bulk.

---

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows are often too "dirty" for a clean health-tech environment. We use **Tonal Layering**.

*   **The Layering Principle:** Depth is achieved by "stacking." A `surface-container-lowest` card placed on a `surface-container-low` background creates a "Ghost Lift"—visible but weightless.
*   **Ambient Shadows:** If a floating element (like a FAB or Tooltip) requires a shadow, use a diffuse blur (30px+) at 5% opacity, using the `primary` color as the shadow tint rather than black.
*   **The Ghost Border Fallback:** If accessibility requires a border, use the `outline_variant` token at **15% opacity**. Never use 100% opaque borders.

---

## 5. Component Guidelines

### Buttons: The Tactile Interaction
*   **Primary:** Rounded `full`. Gradient fill (`primary` to `primary_container`). White text (`on_primary`). No border.
*   **Secondary:** Glass-style. `surface-container-lowest` at 50% opacity with a `backdrop-blur`. 
*   **Tertiary:** Pure text using the `primary` color, with a `title-sm` weight.

### Cards & Lists: The Separation of Data
*   **Rule:** Forbid the use of divider lines. 
*   **Execution:** Separate list items using the Spacing Scale (token `4` or `5`). For grouping, use a slightly different surface tone (e.g., `surface-container-high`) as a soft back-plate for the entire group.
*   **Radius:** All cards must use `xl` (3rem) or `full` radius to maintain the supportive, "soft" brand personality.

### Input Fields: Soft Clarity
*   **Style:** Instead of a box, use a `surface-container-lowest` fill with a `ghost-border`. 
*   **Focus State:** Transition the border to `primary` and add a subtle `primary_fixed_dim` outer glow (4px).

### Health-Specific Components
*   **The "Vitals" Card:** A large-scale card using `display-sm` for the metric, nested inside a `surface-container-lowest` panel with a soft `primary` gradient "glow" in the corner to indicate health status.
*   **Progress Rings:** Use `secondary` for the track and `primary` for the progress, ensuring rounded caps for a friendly feel.

---

## 6. Do’s and Don’ts

### Do:
*   **Do** use extreme whitespace. If a section feels "almost" right, add another `1.4rem` (token `4`) of padding.
*   **Do** use asymmetrical layouts (e.g., a left-aligned headline with a right-aligned floating glass card).
*   **Do** use `primary_container` (#2aa7ff) for background highlights behind iconography to add "Mist-like" depth.

### Don't:
*   **Don't** use pure black (#000000) for text. Always use `on_surface` (#2c2f30) to keep the contrast soft.
*   **Don't** use 1px dividers or "boxes within boxes." Use tonal shifts to define space.
*   **Don't** use sharp corners. If a radius is less than `DEFAULT` (1rem), it is too sharp for this system.
*   **Don't** clutter the screen. If it’s not essential for the user’s immediate health-goal, move it to a secondary layer.