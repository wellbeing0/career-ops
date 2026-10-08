## ADDED Requirements
### Requirement: Consistent control feedback
Enabled hosted controls SHALL expose pointer, visible hover and pressed feedback, keyboard focus and comfortable touch targets; disabled controls SHALL remain distinguishable.
#### Scenario: User presses a button
- **WHEN** a user hovers, focuses or presses an enabled control
- **THEN** its cursor or visible state acknowledges that interaction
### Requirement: Asynchronous action acknowledgement
The UI SHALL acknowledge foreground operations immediately, distinguish busy from saved/error states and indicate active navigation and unsaved profile/CV changes.
#### Scenario: Save or refresh is pending
- **WHEN** a foreground save or refresh starts
- **THEN** an in-progress label appears and duplicate action controls are disabled until completion
