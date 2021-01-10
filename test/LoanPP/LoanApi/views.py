from django.shortcuts import render
from rest_framework import viewsets
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from . forms import ApprovalForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from . models import approvals
from . serializers import approvalsSerializers
import pickle , joblib
import numpy as np
from sklearn import preprocessing
import pandas as pd


class ApprovalsView(viewsets.ModelViewSet):
	queryset = approvals.objects.all()
	serializer_class = approvalsSerializers
def loanform(request):
	if request.method == 'POST':
		form=ApprovalForm(request.POST)
		if form.is_valid():
			Firstname = form.cleaned_data['firstname']
			Lastname = form.cleaned_data['lastname']
			Dependents = form.cleaned_data['Dependents']
			ApplicantIncome = form.cleaned_data['ApplicantIncome']
			CoapplicantIncome = form.cleaned_data['CoapplicantIncome']
			LoanAmount = form.cleaned_data['LoanAmount']
			Loan_Amount_Term = form.cleaned_data['Loan_Amount_Term']
			Credit_History = form.cleaned_data['Credit_History']
			Gender = form.cleaned_data['Gender']
			Married = form.cleaned_data['Married']
			Education = form.cleaned_data['Education']
			Self_Employed = form.cleaned_data['Self_Employed']
			Property_Area = form.cleaned_data['Property_Area']
			myDict = (request.POST).dict()
			df=pd.DataFrame(myDict, index=[0])
			answer=predictor(df)
			print(answer)
			#Xscalers=predictor(ohevalue(df))[1]
			if int(df['LoanAmount'])<25000:
				messages.success(request,'Application Status: {}'.format(answer))
			else:
				messages.success(request,'Invalid: Your Loan Request Exceeds ₹60,00,000 Limit')

	form=ApprovalForm()
	return render(request,'LoanApi/form.html', {'form':form})



def preprocess(df):
	print('Heypreprocess')
	columns = ['Dependents', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
       'Loan_Amount_Term', 'Credit_History', 'Gender_Female', 'Gender_Male',
       'Married_No', 'Married_Yes', 'Property_Area_Rural',
       'Property_Area_Semiurban', 'Property_Area_Urban', 'Self_Employed_No',
       'Self_Employed_Yes', 'Education_Graduate', 'Education_Not Graduate']
	new_df = pd.DataFrame(columns=columns)

	#print(new_df.head())

	df = pd.get_dummies(df,columns=['Gender','Married','Property_Area','Self_Employed','Education'],drop_first = False)
	new_df = new_df.append(df,ignore_index=True)
	new_df.fillna(0,inplace = True)
	
	new_df = new_df[columns]
	new_df = new_df.astype(int)
	#print(new_df.dtypes)
	return new_df


def predictor(unit):
	try:
		print('Heypredictor')
		#model_predictor = pickle.load(open('./xgb', 'rb'))
		model_predictor = joblib.load(r"C:\Users\rushi\Documents\GitHub\LoanPredictionPP\LoanPP\LoanApi\xgb.a")
		X=preprocess(unit)
		y_pred=model_predictor.predict(X)
		print(y_pred)

		newdf=pd.DataFrame(y_pred, columns=['Status'])
		newdf=newdf.replace({'Y':'Approved', 'N':'Rejected'})
		
		print(newdf['Status'][0])
		
		return(newdf['Status'][0])
		#return (newdf.values[0][0],X[0])
	except ValueError as e:
		print('HeyError')
		return (e.args[0])
