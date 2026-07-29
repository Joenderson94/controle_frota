from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required # Importação necessária
from .models import Veiculo, RegistroUso
from .forms import SolicitarVeiculoForm, FinalizarUsoForm


@login_required
def home(request):
    veiculos = Veiculo.objects.all()
    solicitacoes = RegistroUso.objects.all().order_by('-data_solicitacao')[:5]

    contexto = {
        'veiculos': veiculos,
        'solicitacoes': solicitacoes,
    }
    return render(request, 'core/home.html', contexto)

@login_required
def solicitar_veiculo(request):
    if request.method == 'POST':
        form = SolicitarVeiculoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            # Define o motorista logado (ou o usuário padrão se não estiver autenticado ainda)
            if request.user.is_authenticated:
                solicitacao.motorista = request.user
            else:
                # Caso temporário para testes enquanto não configuramos o login
                from django.contrib.auth.models import User
                solicitacao.motorista = User.objects.first()

            solicitacao.save()
            return redirect('home')
    else:
        form = SolicitarVeiculoForm()

    return render(request, 'core/solicitar_veiculo.html', {'form': form})

@login_required
def devolver_veiculo(request, pk):
    # Busca a solicitação pelo ID (pk)
    solicitacao = get_object_or_404(RegistroUso, pk=pk)

    if request.method == 'POST':
        form = FinalizarUsoForm(request.POST, instance=solicitacao)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.status = 'CONCLUIDO'  # Marca como concluído automaticamente
            registro.save()
            return redirect('home')
    else:
        form = FinalizarUsoForm(instance=solicitacao)

    return render(request, 'core/devolver_veiculo.html', {'form': form, 'solicitacao': solicitacao})
