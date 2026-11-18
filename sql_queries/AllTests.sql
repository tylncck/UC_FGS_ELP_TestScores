WITH BaseTest AS (
	SELECT		
		DISTINCT Emplid
		, CAST(Test_Date AS DATE) AS TestDate
		, EnglishTestName = CASE	
			WHEN Test_Component IN ('APIEL')	THEN 'Advanced Placement (AP) International English Language (APIEL)'
			WHEN Test_Component IN ('CAE')		THEN 'Cambridge English Assessment - Advanced (CAE)'
			WHEN Test_Component IN ('CPE')		THEN 'Cambridge English Assessment - Proficiency (CPE)'
			WHEN Test_Component IN ('CAEL')		THEN 'The Canadian Academic English Language (CAEL)'
			WHEN Test_Component IN ('DUOLI')	THEN 'Duolingo'
			WHEN Test_Component IN ('EP190', 'EP193', 'EP197', 'EP220', 'EP225', 'EP230', 'EP235', 'EP249') THEN 'English for Academic Purposes (EAP)'
			WHEN Test_Component IN ('IELTS')	THEN 'International English Language Testing System (IELTS)'
			WHEN Test_Component IN ('PTE')		THEN 'Pearson Test of English (PTE)'
			WHEN Test_Component IN ('TOEFC', 'TOEFP', 'TOEFI')	THEN 'Test of English as a Foreign Language (TOEFL)'
			WHEN Test_Component IN ('MELAB')	THEN 'Michigan English Language Assessment Battery (MELAB)'
			WHEN Test_Component IN ('TWE')		THEN 'Test of Written English (TWE)'
			WHEN Test_Component IN ('TSE')		THEN 'Test of Spoken English (TSE)' 
			ELSE	'Test Component' END
	FROM		
		F_External_Tests AS FET

	WHERE		
		Test_ID = 'ELP'
		AND Best_Score_Ind = 'Y'
		AND Test_Date >= '2020-01-01'
)

SELECT		
	*
FROM		
	BaseTest 
WHERE		
	EnglishTestName != 'Test Component'