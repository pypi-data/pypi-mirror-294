! This automatically generated Fortran wrapper file allows codes
! written in Fortran to be called directly from C and translates all
! C-style arguments into expected Fortran-style arguments (with
! assumed size, local type declarations, etc.).


MODULE C_FMATH
USE ISO_FORTRAN_ENV , ONLY : RT => REAL32
  IMPLICIT NONE


CONTAINS


  
  SUBROUTINE C_ORTHONORMALIZE(A_DIM_1, A_DIM_2, A, LENGTHS_DIM_1, LENGTHS) BIND(C)
    USE FMATH, ONLY: ORTHONORMALIZE
    IMPLICIT NONE
    INTEGER(KIND=SELECTED_INT_KIND(18)), INTENT(IN) :: A_DIM_1
    INTEGER(KIND=SELECTED_INT_KIND(18)), INTENT(IN) :: A_DIM_2
    REAL(KIND=RT), INTENT(INOUT), DIMENSION(A_DIM_1,A_DIM_2) :: A
    INTEGER(KIND=SELECTED_INT_KIND(18)), INTENT(IN) :: LENGTHS_DIM_1
    REAL(KIND=RT), INTENT(OUT), DIMENSION(LENGTHS_DIM_1) :: LENGTHS
  
    CALL ORTHONORMALIZE(A, LENGTHS)
  END SUBROUTINE C_ORTHONORMALIZE
  
END MODULE C_FMATH

