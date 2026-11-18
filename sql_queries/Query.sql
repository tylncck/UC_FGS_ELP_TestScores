WITH BaseTest AS (
	SELECT		
		DISTINCT Emplid
		, CAST(Test_Date AS DATE) AS TestDate
		, EnglishTestName = CASE	
			WHEN Test_Component IN ('APIEL')	THEN 'APIEL'
			WHEN Test_Component IN ('CAE')		THEN 'CAE'
			WHEN Test_Component IN ('CPE')		THEN 'CPE'
			WHEN Test_Component IN ('CAEL')		THEN 'CAEL'
			WHEN Test_Component IN ('DUOLI')	THEN 'Duolingo'
			WHEN Test_Component IN ('EP190', 'EP193', 'EP197', 'EP220', 'EP225', 'EP230', 'EP235', 'EP249') THEN 'EAP'
			WHEN Test_Component IN ('IELTS')	THEN 'IELTS'
			WHEN Test_Component IN ('PTE')		THEN 'PTE'
			WHEN Test_Component IN ('TOEFC', 'TOEFP', 'TOEFI')	THEN 'TOEFL'
			WHEN Test_Component IN ('MELAB')	THEN 'MELAB'
			WHEN Test_Component IN ('TWE')		THEN 'TWE'
			WHEN Test_Component IN ('TSE')		THEN 'TSE' 
			ELSE	'Test Component' END
	FROM		
		F_External_Tests AS FET

	WHERE		
		Test_ID = 'ELP'
		AND Best_Score_Ind = 'Y'
		AND Test_Date >= '2020-01-01'
)

, EnlglishTests AS (
	SELECT		
		*
	FROM		
		BaseTest 
	WHERE		
		EnglishTestName != 'Test Component'
)

, EnglishTestOrdered AS (
	SELECT		
		*
		, RowNumber = ROW_NUMBER() OVER(PARTITION BY Emplid ORDER BY TestDate DESC)
	FROM		
		EnlglishTests
)

, EnglishTestLatest AS (
	SELECT		
		Emplid, 
		TestDate, 
		EnglishTestName
	FROM
		EnglishTestOrdered
	WHERE		
		RowNumber = 1
)

, WithdrawalData AS (
	SELECT		
		DISTINCT Admission_Application_Nbr
	FROM		
		D_Student_Career_Term
	WHERE		
		Admit_Term >= 2201
		AND Academic_Career = 'GRAD'
		AND Withdraw_Code_Desc IN ('Cancelled', 'Withdrew')
		AND	Academic_Program IN ('GSDOC', 'GSMTH', 'GSMCB')
		AND Tuition_Residency = 'INTL'
)

, EnrolmentData AS (
	SELECT		
		Emplid
		, Cumulative_GPA
		, Academic_Program
		--, AVG(Cumulative_GPA) AS Cumulative_GPA
		, Discontinuation = CASE WHEN Admission_Application_Nbr IN (SELECT * FROM WithdrawalData) THEN 1 ELSE 0 END
		, RowNumber = ROW_NUMBER() OVER(PARTITION BY Admission_Application_Nbr ORDER BY Term DESC)
	FROM		
		F_Student_Career_Term AS FSCT
	WHERE		
		Admit_Term >= 2201
		AND Academic_Career = 'GRAD'
		AND Academic_Program IN ('GSDOC', 'GSMCB', 'GSMTH')
		AND Registered_Ind = 'Y'
		AND Tuition_Residency = 'INTL'
		AND Cumulative_GPA > 0
	--GROUP BY 	Emplid,
	--			Academic_Program
)

, EnrolmentLasestTerm AS (
	SELECT	
		Emplid
		, Academic_Program
		, Discontinuation
		, Cumulative_GPA
	FROM	
		EnrolmentData
	WHERE
		RowNumber = 1
)

, EnrolmentEnglishTest AS (
	SELECT		
		ED.Emplid
		, ED.Cumulative_GPA
		, ED.Academic_Program
		, ED.Discontinuation
		, TestName = CASE WHEN ET.EnglishTestName IS NULL THEN 'No Test' ELSE ET.EnglishTestName END
	FROM		
		EnrolmentLasestTerm AS ED

	LEFT JOIN	
		EnglishTestLatest AS ET
	ON	
		ET.Emplid = ED.Emplid
)

--SELECT		Emplid, COUNT(*)
--FROM		EnrolmentEnglishTest
--GROUP BY	Emplid
--HAVING		COUNT(*) >= 2

--SELECT		SUM(Discontinuation) AS Discontinuation, COUNT(*) AS Total, SUM(Discontinuation) * 1.0 / COUNT(*) AS Ratio 
--FROM		EnrolmentEnglishTest

SELECT		
	*
FROM		
	EnrolmentEnglishTest
